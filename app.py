"""
The purpose of this API is to easily link between
a Wikipedia article and the corresponding Wikicitations item
https://rapidapi.com/blog/how-to-build-an-api-in-python/
"""
import logging

from flask import Flask
from flask_restful import Api, Resource

import config
from models.lookup_wikicitations_qid import LookupWikicitationsQid
from models.send_job_to_rabbitmq import SendJobToRabbitmq

logging.basicConfig(level=config.loglevel)

app = Flask(__name__)
api = Api(app)


class LookupByWikidataQid(Resource):
    @staticmethod
    def get(qid=""):
        if qid:
            lwq = LookupWikicitationsQid()
            return lwq.lookup_via_query_service(wdqid=qid), 200
        else:
            return "No Wikidata QID was given", 400


class AddJobToQueue(Resource):
    @staticmethod
    def get(qid=""):
        if qid:
            queue = SendJobToRabbitmq()
            return queue.publish_job(wdqid=qid), 200
        else:
            return "No Wikidata QID was given", 400

#api.add_resource(LookupByLabel, "/lookup-by-label/<str:label>")
api.add_resource(LookupByWikidataQid, "/wikidata-qid/<string:qid>")
api.add_resource(AddJobToQueue, "/add-job/<string:qid>")

if __name__ == '__main__':
    app.run(debug=True)