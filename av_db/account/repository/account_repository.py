from abc import ABC, abstractmethod


class AccountRepository(ABC):

    @abstractmethod
    def save(self, email, loginType):
        pass

    @abstractmethod
    def saveAdmin(self, email):
        pass

    @abstractmethod
    def findById(self, accountId):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def deleteAccount(self, accountId: int) -> bool:
        pass
