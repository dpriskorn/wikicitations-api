import logging
from typing import Optional

import backoff
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from pydantic import validate_arguments, BaseModel

import config

logger = logging.getLogger(__name__)


class NoChannelError(BaseException):
    pass


class WorkQueue(BaseModel):
    """This models the RabbitMQ article queue
    We publish to this queue when ingesting page updates
    and when receiving a WDQID via the wikicitaitons-api"""

    connection: Optional[BlockingConnection]
    channel: Optional[BlockingChannel]
    queue_name: str = "article_queue"

    class Config:
        arbitrary_types_allowed = True

    @validate_arguments
    def publish(self, message: bytes):
        """This publishes a message to the default work queue"""
        self.__connect__()
        self.__setup_channel__()
        self.__create_queue__()
        self.__send_message__(message=message)
        self.__close_connection__()

    @backoff.on_exception(backoff.expo, AMQPConnectionError, max_time=60)
    def __connect__(self):
        self.connection = BlockingConnection(
            ConnectionParameters(
                "localhost",
                credentials=PlainCredentials(
                    username=config.rabbitmq_username, password=config.rabbitmq_password
                ),
            )
        )

    def __setup_channel__(self):
        self.channel = self.connection.channel()

    def __create_queue__(self):
        self.channel.queue_declare(queue=self.queue_name)

    def __close_connection__(self):
        self.connection.close()

    def __send_message__(self, message: bytes):
        if self.channel:
            self.channel.basic_publish(
                exchange="", routing_key=self.queue_name, body=message
            )
            print(" [x] Sent message!")
        else:
            raise NoChannelError()
