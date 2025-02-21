from abc import ABC, abstractmethod


class AccountProfileRepository(ABC):
    @abstractmethod
    def save(self, account, nickname):
        pass

    @abstractmethod
    def findByAccount(self, account):
        pass

    @abstractmethod
    def findById(self, accountId):
        pass

    def findByPassword(self, email,password):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def findByNickname(self, nickname):
        pass


    @abstractmethod
    def findGenderTypeByGenderId(self, genderId):
        pass