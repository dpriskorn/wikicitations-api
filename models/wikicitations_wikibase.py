from models.wikibase import Wikibase


class WikiCitationsWikibase(Wikibase):
    """This models the properties and items on wikicitations.wikibase.cloud"""
    title = "wikicitations.wikibase.cloud"
    wikibase_url = "https://wikicitations.wikibase.cloud"
    query_service_url = wikibase_url + "/query/"
    WIKIDATA_QID = "P62"  # datatype: WikibaseDatatype.EXTERNALID description: None
