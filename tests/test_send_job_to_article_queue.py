from unittest import TestCase

from pydantic import ValidationError

from models.send_job_to_article_queue import SendJobToArticleQueue


class TestSendJobToArticleQueue(TestCase):
    def test_publish_job_missing_everything(self):
        with self.assertRaises(ValidationError):
            SendJobToArticleQueue()  # type: ignore # mypy: ignore

    def test_publish_job(self):
        queue = SendJobToArticleQueue(
            language_code="en", wikimedia_site="wikipedia", title="Test", testing=True
        )
        assert queue.publish_to_article_queue() is True
