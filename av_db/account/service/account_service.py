from abc import ABC, abstractmethod


class AccountService(ABC):
    @abstractmethod
    def createAccount(self, email, gender, birthyear, loginType):
        pass

    @abstractmethod
    def checkEmailDuplication(self, email):
        pass

    @abstractmethod
    def findEmail(self, accountId):
        pass
