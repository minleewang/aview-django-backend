from abc import ABC, abstractmethod

class CompanyReportRepository(ABC):

    @abstractmethod
    def createMany(self, reportDataList):
        pass

    @abstractmethod
    def findAll(self):
        pass
