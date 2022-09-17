from unittest import TestCase

from models.wikicitations_wikibase import WikiCitationsWikibase


class TestWikiCitationsWikibase(TestCase):
    def test_valid_qid_invalid_input(self):
        wcw = WikiCitationsWikibase()
        assert wcw.is_valid_qid(qid="123") is False

    def test_valid_qid_valid_input(self):
        wcw = WikiCitationsWikibase()
        assert wcw.is_valid_qid(qid="Q123") is True

    def test_valid_qid_valid_input_lowercase(self):
        wcw = WikiCitationsWikibase()
        assert wcw.is_valid_qid(qid="q123") is True

    def test_valid_qid_invalid_input_alpha(self):
        wcw = WikiCitationsWikibase()
        assert wcw.is_valid_qid(qid="q123a") is False
