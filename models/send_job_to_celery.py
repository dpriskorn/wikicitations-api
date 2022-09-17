from models.enums import Return
from models.wikicitations_wikibase import WikiCitationsWikibase


class SendJobToCelery:
    wikibase = WikiCitationsWikibase()
    def __add_job_to_work_queue__(self):
        raise NotImplementedError()

    def __connect__(self):
        """Connect"""
        raise NotImplementedError()

    def publish_job(self, wdqid=""):
        """Connect and publish the job"""
        if wdqid:
            if self.wikibase.is_valid_qid(qid=wdqid):
                self.__connect__()
                self.__add_job_to_work_queue__()
            else:
                return Return.INVALID_QID
        else:
            return Return.NO_QID