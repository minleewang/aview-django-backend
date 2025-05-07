from abc import ABC, abstractmethod

class InterviewResultService(ABC):
    @abstractmethod
    def saveInterviewResult(self, accountId, userToken, summary, questions, answers):
        pass


    @abstractmethod
    def getInterviewResult(self, userToken):
        pass

    @abstractmethod
    def getFullQAList(self, interviewId):
        pass


