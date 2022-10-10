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
from models.send_job_to_article_queue import SendJobToArticleQueue

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


class AddJobToQueue(Resource):
    @staticmethod
    def get(language_code: str = "", title: str = "", wikimedia_site: str = ""):
        # TODO handle URL encoding of the title
        if language_code == "en" and title and wikimedia_site == "wikipedia":
            queue = SendJobToArticleQueue(language_code=language_code, title=title, wikimedia_site=wikimedia_site)
            return queue.publish_to_article_queue(), 200
        else:
            # Something was not valid, return a meaningful error
            if language_code != "en":
                return "Only en language code is supported", 400
            if title == "":
                return "Title was missing", 400
            if wikimedia_site != "wikipedia":
                return "Only 'wikipedia' site is supported", 400


api.add_resource(LookupByWikidataQid, "/wikidata-qid/<string:qid>")
api.add_resource(AddJobToQueue, "/add-job/<string:language_code>/<string:wikimedia_site>/title")

if __name__ == "__main__":
    app.run(debug=True)
