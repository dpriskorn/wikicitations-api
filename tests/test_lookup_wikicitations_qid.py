import logging
from unittest import TestCase

import config
from models.enums import Return
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

    def test_lookup_via_query_service_invalid_qid(self):
        lwq = LookupWikicitationsQid()
        wcdqid = lwq.lookup_via_query_service(wdqid="aQ14452")
        assert wcdqid == Return.INVALID

    def test_lookup_via_query_service_invalid_qid_2(self):
        lwq = LookupWikicitationsQid()
        wcdqid = lwq.lookup_via_query_service(wdqid="aQ14452a")
        assert wcdqid == Return.INVALID

    def test_lookup_via_query_service_invalid_qid_3(self):
        lwq = LookupWikicitationsQid()
        wcdqid = lwq.lookup_via_query_service(wdqid="3Q14452")
        assert wcdqid == Return.INVALID

    def test_lookup_via_query_service_no_qid(self):
        lwq = LookupWikicitationsQid()
        wcdqid = lwq.lookup_via_query_service(wdqid="")
        assert wcdqid == Return.NO_QID
