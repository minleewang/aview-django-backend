from abc import ABC, abstractmethod


class AccountProfileRepository(ABC):

    @abstractmethod
    def save(self, account, nickname, gender, birthyear, age_range):
        pass

    @abstractmethod
    def findByAccount(self, account):
        pass
