from unittest import TestCase

from models.enums import Return
from models.send_job_to_celery import SendJobToCelery


class TestSendJobToRabbitmq(TestCase):
    def test_publish_job_missing_qid(self):
        queue = SendJobToCelery()
        assert queue.publish_job() == Return.NO_QID

    def test_publish_job_valid_qid(self):
        queue = SendJobToCelery()
        with self.assertRaises(NotImplementedError):
            queue.publish_job(wdqid="Q1")