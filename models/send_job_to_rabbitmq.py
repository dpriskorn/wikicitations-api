from models.exceptions import MissingInformationError


class SendJobToRabbitmq:
    def __add_job_to_work_queue__(self):
        raise NotImplementedError()

    def __connect__(self):
        """Connect to rabbitmq"""
        raise NotImplementedError()
    def publish_job(self, wdqid=""):
        """Connect to rabbitmq and publish the job"""
        if wdqid:
            self.__connect__()
            self.__add_job_to_work_queue__()
        else:
            raise MissingInformationError("no wdqid given")