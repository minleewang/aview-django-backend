from abc import ABC, abstractmethod

class InterviewTechStackService(ABC):

    @abstractmethod
    def get_all_tech_stacks(self):
        pass
