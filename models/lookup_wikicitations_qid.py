import logging

from pydantic import BaseModel
from wikibaseintegrator import wbi_config, WikibaseIntegrator, wbi_helpers
from wikibaseintegrator.wbi_helpers import execute_sparql_query

import config
from helpers import console
from models.exceptions import MissingInformationError
from models.wikicitations_wikibase import WikiCitationsWikibase

logger = logging.getLogger(__name__)

class LookupWikicitationsQid(BaseModel):
    wikibase = WikiCitationsWikibase()
    # lookup the wcdqid based on the wdqid
    def __setup_wikibase_integrator_configuration__(
        self,
    ) -> None:
        wikibase = WikiCitationsWikibase()
        wbi_config.config["USER_AGENT"] = config.user_agent
        wbi_config.config["WIKIBASE_URL"] = wikibase.wikibase_url
        wbi_config.config["MEDIAWIKI_API_URL"] = wikibase.mediawiki_api_url
        wbi_config.config["MEDIAWIKI_INDEX_URL"] = wikibase.mediawiki_index_url
        wbi_config.config["SPARQL_ENDPOINT_URL"] = wikibase.sparql_endpoint_url

    def lookup_via_query_service(self, wdqid="") -> str:
        """This looks up the WDQID via the query service. It is slower than using cirrussearch"""
        if wdqid:
            self.__setup_wikibase_integrator_configuration__()
            property = self.wikibase.WIKIDATA_QID
            query = f"""
            prefix wcd: <{self.wikibase.rdf_prefix}/entity/>
            prefix wcdt: <{self.wikibase.rdf_prefix}/prop/direct/>
                SELECT ?item WHERE {{
                  ?item wcdt:{property} "{wdqid}".
                }}
            """
            result = execute_sparql_query(query=query)
            console.print(result)
            # TODO parse the result and get the wcdqid out
            wcdqids = self.wikibase.extract_item_ids(sparql_result=result)
            logger.info(f"Found {wcdqids}")
            for wcdqid in wcdqids:
                # We only ever care about the first
                return wcdqid
        else:
            raise MissingInformationError("no wdqid given")

    def lookup_via_cirrussearch(self, wdqid=""):
        """This does not work because the WikibaseCirrusSearch
        extension is not enabled yet on our Wikibases in Wikibase.cloud"""
        raise Exception("This does not work because the WikibaseCirrusSearch "
                        "extension is not enabled yet on our Wikibases in Wikibase.cloud")
        # # TODO check if valid
        # self.__setup_wikibase_integrator_configuration__()
        # wbi = WikibaseIntegrator()
        # data = {
        #     'action': 'query',
        #     'list': 'search',
        #     'srsearch': f'haswbstatement:{config.wikidata_qid_property}={wdqid}',
        # }
        # result = wbi_helpers.mediawiki_api_call_helper(data=data, allow_anonymous=True, user_agent=config.user_agent)
        # #console.print(result)
        # #console.print(result.get("query"))
        # if result.get("query"):
        #     logger.debug("got query")
        #     if result.get("query").get("searchinfo"):
        #         logger.debug("got searchinfo")
        #         totalhits = int(result.get("query").get("searchinfo").get("totalhits"))
        #         if totalhits:
        #             logger.debug("got totalhits > 0")
        #             first_hit = result.get("query").get("search")[0]
        #             console.print(first_hit)
        #             return first_hit
        #         else:
        #             message = "No hit for this qid in Wikicitations"
        #             logger.info(message)
        #             return message