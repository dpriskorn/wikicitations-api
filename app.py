"""
The purpose of this API is to easily link between
a Wikipedia article and the corresponding Wikicitations item
https://rapidapi.com/blog/how-to-build-an-api-in-python/
"""
import logging
from typing import Union

from flask import Flask
from flask_restful import Api, Resource

import config
from models.enums import Return
from models.lookup_wikicitations_qid import LookupWikicitationsQid

logging.basicConfig(level=config.loglevel)

app = Flask(__name__)
api = Api(app)


class LookupByWikidataQid(Resource):
    def get(self, qid=""):
        if qid:
            lwq = LookupWikicitationsQid()
            result: Union[Return, str] = lwq.lookup_via_query_service(wdqid=qid)
            if isinstance(result, str):
                return result, 200
            elif result == Return.NO_MATCH:
                return result.value, 404
            else:
                return result.value, 400
        else:
            return Return.NO_QID.value, 400


# api.add_resource(LookupByLabel, "/lookup-by-label/<str:label>")
api.add_resource(LookupByWikidataQid, "/wikidata-qid/<string:qid>")

if __name__ == "__main__":
    app.run(debug=True)
