from unittest import TestCase

from models.send_job_to_rabbitmq import SendJobToRabbitmq


class TestSendJobToRabbitmq(TestCase):
    def test_publish_job(self):
        queue = SendJobToRabbitmq()
        with self.assertRaises(NotImplementedError):
            queue.publish_job()