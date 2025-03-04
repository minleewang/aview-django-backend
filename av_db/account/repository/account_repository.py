from abc import ABC, abstractmethod


class AccountRepository(ABC):
    @abstractmethod
    def create(self, account_profile):
        pass


    @abstractmethod
    def findById(self, accountId):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def findByNickname(self, nickname):
        pass

    @abstractmethod
    def findByRoleType(self, roleType):
        pass






    #@abstractmethod
    #def withdrawAccount(self, account, withdrawReason):
    #    pass