from abc import ABC, abstractmethod


class GuestAccountService(ABC):

    # DB 생성
    @abstractmethod
    def createGuestAccount(self, email, loginType):
        pass

    # MyPage 수정칸
    @abstractmethod
    def findEmail(self, guestAccountId):
        pass
