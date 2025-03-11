from abc import ABC, abstractmethod


class AccountRepository(ABC):

    @abstractmethod
    def save(self, email, gender, age_range, birthyear, loginType):
        pass

    @abstractmethod
    def findById(self, accountId):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass