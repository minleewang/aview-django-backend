from abc import ABC, abstractmethod

class InterviewResultService(ABC):
    @abstractmethod
    def saveInterviewResult(self, accountId):
        pass


    @abstractmethod
    def getInterviewResult(self, userToken):
        pass


