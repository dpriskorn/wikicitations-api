from pydantic import validate_arguments

from models.wikibase import Wikibase


class WikiCitationsWikibase(Wikibase):
    """This models the properties and items on wikicitations.wikibase.cloud"""

    title = "wikicitations.wikibase.cloud"
    wikibase_url = "https://wikicitations.wikibase.cloud"
    query_service_url = wikibase_url + "/query/"
    WIKIDATA_QID = "P62"  # datatype: WikibaseDatatype.EXTERNALID description: None

    @validate_arguments
    def is_valid_qid(self, qid: str) -> bool:
        """Validate the qid"""
        if qid[:1].upper() == "Q" and qid[1:].isnumeric():
            return True
        else:
            return False
