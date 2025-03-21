from abc import ABC, abstractmethod


class AccountService(ABC):

    # DB 생성
    @abstractmethod
    def createAccount(self, email, loginType):
        pass
    @abstractmethod
    def createAdminAccount(self, email, loginType):
        pass

    # 이메일 중복확인
    @abstractmethod
    def checkEmailDuplication(self, email):
        pass


    # MyPage 수정칸
    @abstractmethod
    def findEmail(self, accountId):
        pass

    # 회원탈퇴
    @abstractmethod
    def withdraw(self, accountId: int) -> bool:
        pass
