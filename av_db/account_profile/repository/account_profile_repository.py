from abc import ABC, abstractmethod


class AccountProfileRepository(ABC):

    @abstractmethod
    def save(self, nickname, email, gender, age_range, birthyear, loginType):
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



    #@abstractmethod
    #def updateLastLogin(self, profile):
    #    pass

    #@abstractmethod
    #def update_login_history(self, profile):
    #    pass