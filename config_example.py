import logging

user_agent = "wikicitations-api"
wikidata_qid_property = (
    "P62"  # see https://wikicitations.wikibase.cloud/wiki/Special:ListProperties
)
loglevel = logging.INFO

# Login to rabbitmq bitnami container
rabbitmq_username = ""
rabbitmq_password = ""
