from abc import ABC, abstractmethod


class AccountService(ABC):
    @abstractmethod
    def createAccount(self, email, loginType):
        pass

    @abstractmethod
    def createAdminAccount(self, email, loginType):
        pass

    @abstractmethod
    def checkEmailDuplication(self, email):
        pass

    @abstractmethod
    def findEmail(self, accountId):
        pass

    @abstractmethod
    def withdraw(self, accountId: int) -> bool:
        pass
