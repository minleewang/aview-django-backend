from abc import ABC, abstractmethod


class AccountProfileService(ABC):
    @abstractmethod
    def createAccountProfile(self, accountId, nickname, gender, birthyear, age_range):
        pass

    @abstractmethod
    def createAdminProfile(self, accountId, email):
        pass
