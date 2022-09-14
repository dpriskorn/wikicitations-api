import logging
from unittest import TestCase

import config
from models.lookup_wikicitations_qid import LookupWikicitationsQid

logging.basicConfig(level=config.loglevel)

class TestLookupWikicitationsQid(TestCase):
    # def test_lookup_via_cirrussearch((self):
    #     lwq = LookupWikicitationsQid()
    #     lwq.lookup_via_cirrussearch(wdqid="Q1")

    def test_lookup_via_query_service(self):
        lwq = LookupWikicitationsQid()
        wcdqid = lwq.lookup_via_query_service(wdqid="Q14452")
        assert wcdqid == "Q8243"