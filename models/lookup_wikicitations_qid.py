import logging

from pydantic import BaseModel
from wikibaseintegrator import wbi_config, WikibaseIntegrator, wbi_helpers

import config
from helpers import console
from models.wikicitations_wikibase import WikiCitationsWikibase

logger = logging.getLogger(__name__)

class LookupWikicitationsQid(BaseModel):
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

    def lookup(self, wdqid=""):
        # TODO check if valid
        self.__setup_wikibase_integrator_configuration__()
        wbi = WikibaseIntegrator()
        data = {
            'action': 'query',
            'list': 'search',
            'srsearch': f'haswbstatement:{config.wikidata_qid_property}={wdqid}',
        }
        result = wbi_helpers.mediawiki_api_call_helper(data=data, allow_anonymous=True, user_agent=config.user_agent)
        #console.print(result)
        #console.print(result.get("query"))
        if result.get("query"):
            logger.debug("got query")
            if result.get("query").get("searchinfo"):
                logger.debug("got searchinfo")
                totalhits = int(result.get("query").get("searchinfo").get("totalhits"))
                if totalhits:
                    logger.debug("got totalhits > 0")
                    first_hit = result.get("query").get("search")[0]
                    console.print(first_hit)
                    return first_hit
                else:
                    message = "No hit for this qid in Wikicitations"
                    logger.info(message)
                    return message