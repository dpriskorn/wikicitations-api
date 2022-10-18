"""
The purpose of this API is to easily link between
a Wikipedia article and the corresponding Wikicitations item
https://rapidapi.com/blog/how-to-build-an-api-in-python/
"""
import logging
from typing import Union, Optional

from flask import Flask, request
from flask_restful import Api, Resource, abort

import config
from helpers import console
from models.add_job_schema import AddJobSchema
from models.enums import Return
from models.job import Job
from models.lookup_wikicitations_qid import LookupWikicitationsQid
from models.send_job_to_article_queue import SendJobToArticleQueue

logging.basicConfig(level=config.loglevel)
logger = logging.getLogger(__name__)
app = Flask(__name__)
api = Api(app, prefix="/v1")


class LookupByWikidataQid(Resource):
    @staticmethod
    def get(qid=""):
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
    schema = AddJobSchema()
    job: Optional[Job]

    def get(self):
        self.__validate_and_get_job__()
        # TODO handle URL encoding of the title
        if self.job.lang == "en" and self.job.title and self.job.site == "wikipedia":
            queue = SendJobToArticleQueue(
                language_code=self.job.lang,
                title=self.job.title,
                wikimedia_site=self.job.site,
            )
            logger.info("Publishing to queue")
            if self.job.testing:
                return "ok", 200
            else:
                queued = queue.publish_to_article_queue()
                if queued:
                    return "job queued", 201
                else:
                    return "server error, the job could not be queued", 500
        else:
            # Something was not valid, return a meaningful error
            logger.error("did not get what we need")
            if self.job.lang != "en":
                return "Only en language code is supported", 400
            if self.job.title == "":
                return "Title was missing", 400
            if self.job.site != "wikipedia":
                return "Only 'wikipedia' site is supported", 400

    def __validate_and_get_job__(self):
        self.__validate__()
        self.__parse_into_job__()

    def __validate__(self):
        errors = self.schema.validate(request.args)
        if errors:
            abort(400, error=str(errors))

    def __parse_into_job__(self):
        console.print(request.args)
        self.job = self.schema.load(request.args)
        console.print(self.job.dict())


api.add_resource(LookupByWikidataQid, "/wikidata-qid/<string:qid>")
api.add_resource(
    AddJobToQueue, "/add-job"
)  # ?lang=<string:language_code>&site=<string:wikimedia_site>&title=<string:title>")

if __name__ == "__main__":
    app.run(debug=True)
