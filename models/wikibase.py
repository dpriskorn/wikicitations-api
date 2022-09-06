from pydantic import BaseModel, validate_arguments


class Wikibase(BaseModel):
    """This is a parent class for the wikibases we support
    We define all the properties here to be able to use them in the subclasses"""

    #botpassword: str
    item_prefixed_wikibase = True
    query_service_url: str
    title: str
    #user_name: str
    wikibase_cloud_wikibase: bool = True
    wikibase_url: str

    @property
    def mediawiki_api_url(self) -> str:
        return self.wikibase_url + "/w/api.php"

    @property
    def mediawiki_index_url(self) -> str:
        return self.wikibase_url + "/w/index.php"

    @property
    def rdf_entity_prefix(self) -> str:
        return self.rdf_prefix + "/entity/"

    @property
    def rdf_prefix(self) -> str:
        """We only support wikibase.cloud Wikibase installations for now"""
        return self.wikibase_url

    @property
    def sparql_endpoint_url(self) -> str:
        if self.wikibase_cloud_wikibase:
            """This is the default endpoint url for Wikibase.cloud instances"""
            return self.wikibase_url + "/query/sparql"
        else:
            """This is the default docker Wikibase endpoint url
            Thanks to @Myst for finding/documenting it."""
            return self.query_service_url + "/proxy/wdqs/bigdata/namespace/wdq/sparql"

    @validate_arguments
    def entity_history_url(self, item_id: str):
        if self.item_prefixed_wikibase:
            return (
                f"{self.wikibase_url}/w/index.php?title=Item:{item_id}&action=history"
            )
        else:
            return f"{self.wikibase_url}/w/index.php?title={item_id}&action=history"

    @validate_arguments
    def entity_url(self, item_id: str):
        if self.item_prefixed_wikibase:
            return f"{self.wikibase_url}/wiki/Item:{item_id}"
        else:
            return f"{self.wikibase_url}/wiki/{item_id}"
