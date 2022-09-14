from typing import Dict, Optional, Iterable

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

    @validate_arguments
    def __extract_wcdqs_json_entity_id__(
        self, data: Dict, sparql_variable: str = "item"
    ) -> str:
        """We default to "item" as sparql value because it is customary in the Wikibase ecosystem"""
        return str(
            data[sparql_variable]["value"].replace(self.rdf_entity_prefix, "")
        )

    @validate_arguments
    def extract_item_ids(self, sparql_result: Optional[Dict]) -> Iterable[str]:
        """Yield item ids from a sparql result"""
        if sparql_result:
            yielded = 0
            for binding in sparql_result["results"]["bindings"]:
                if item_id := self.__extract_wcdqs_json_entity_id__(data=binding):
                    yielded += 1
                    yield item_id
            if number_of_bindings := len(sparql_result["results"]["bindings"]):
                logger.info(f"Yielded {yielded} bindings out of {number_of_bindings}")
