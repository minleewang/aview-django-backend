from abc import ABC, abstractmethod


class AccountService(ABC):


    @abstractmethod
    def createAccount(self, nickname, email, loginType):
        pass



    @abstractmethod
    def findAccountById(self, accountId):
        pass

    @abstractmethod
    def findAccountByEmail(self, email):
        pass

    @abstractmethod
    def findAccountByRoleType(self, roleType):
        pass

    @abstractmethod
    def findAccountByNickname(self, nickname):
        pass




    #@abstractmethod
    #def findProfileByEmail(self,email):
    #    pass

    #@abstractmethod
    #def withdrawAccount(self, accountId):
    #    pass