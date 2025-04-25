from abc import ABC, abstractmethod


class GuestAccountRepository(ABC):

    @abstractmethod
    def save(self, email, loginType):
        pass

    @abstractmethod
    def findById(self, guestAccountId):
        pass

    @abstractmethod
    def findByEmail(self, email):
        pass