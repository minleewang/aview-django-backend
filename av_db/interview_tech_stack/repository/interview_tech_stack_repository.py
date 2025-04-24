from abc import ABC, abstractmethod

class InterviewTechStackRepository(ABC):

    @abstractmethod
    def find_all(self):
        pass
