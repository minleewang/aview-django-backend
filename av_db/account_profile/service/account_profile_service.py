from abc import ABC, abstractmethod


class AccountProfileService(ABC):
    @abstractmethod
    def createAccountProfile(self, nickname, email, gender, age_range, birthyear, loginType):
        pass


    @abstractmethod
    def checkEmailDuplication(self, email):
        pass

    @abstractmethod
    def checkNicknameDuplication(self, nickname):
        pass



    @abstractmethod
    def findProfileById(self, accountId):
        pass

    @abstractmethod
    def findProfileByEmail(self,email):
        pass
    # 이메일 찾아서 뭐해? 용도가 뭘까: 계정 찾기 (ID 찾기)  -> 프론트에서 아이디 찾는 창 만들기



