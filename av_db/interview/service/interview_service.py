from abc import ABC, abstractmethod


class InterviewService(ABC):

    @abstractmethod
    def createInterview(self, accountId, jobCategory, experienceLevel):
        pass

    @abstractmethod
    def listInterview(self, accountId, page, pageSize):
        pass

    @abstractmethod
    def removeInterview(self, accountId, interviewId):
        pass
