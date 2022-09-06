import logging
from unittest import TestCase

import config
from models.lookup_wikicitations_qid import LookupWikicitationsQid

logging.basicConfig(level=config.loglevel)

class TestLookupWikicitationsQid(TestCase):
    def test_lookup(self):
        lwq = LookupWikicitationsQid()
        lwq.lookup(wdqid="Q1")
