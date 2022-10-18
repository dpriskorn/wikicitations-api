from unittest import TestCase

from pydantic import ValidationError

from models.work_queue import WorkQueue


class TestWorkQueue(TestCase):
    def test_publish_no_message(self):
        wq = WorkQueue()
        with self.assertRaises(ValidationError):
            assert wq.publish() is True

    # def test_publish(self):
    #     wq = WorkQueue()
    #     assert wq.publish(message=Message()) is True