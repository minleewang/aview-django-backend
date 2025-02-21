from abc import ABC, abstractmethod


class AccountProfileService(ABC):
    @abstractmethod
    def createAccountProfile(self, nickname, email, password, salt, gender, birthyear, account):
        pass

    @abstractmethod
    def registerAccount(self, loginType, roleType, nickname, email, password, salt, gender, birthyear):
        pass

    @abstractmethod
    def checkEmailDuplication(self, email):
        pass

    @abstractmethod
    def checkNicknameDuplication(self, nickname):
        pass

    @abstractmethod
    def checkPasswordDuplication(self, email, password):
        pass

    @abstractmethod
    def findProfileByEmail(self,email):
        pass



