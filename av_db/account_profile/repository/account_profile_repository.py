from abc import ABC, abstractmethod


class AccountProfileRepository(ABC):

    @abstractmethod
    def save(self, account, nickname, gender, birthyear, age_range):
        pass

    @abstractmethod
    def findByAccount(self, account):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass

    @abstractmethod
    def findByRoleType(self, roleType):
        pass

    @abstractmethod
    def findByNickname(self, nickname):
        pass

    @abstractmethod
    def findByGender(self, gender):
        pass

    @abstractmethod
    def findByBirthyear(self, birthyear):
        pass
