from account.repository.account_repository_impl import AccountRepositoryImpl
# from account_profile.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from account_profile.service.account_profile_service import AccountProfileService


class AccountProfileServiceImpl(AccountProfileService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__accountProfileRepository = AccountProfileRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    # AccountProfile DB 생성하고 카카오에서 받은 정보 저장
    def createAccountProfile(self, nickname, email, gender, age_range, birthyear, loginType):
        return self.__accountProfileRepository.save(nickname, email, gender, age_range, birthyear, loginType)
        # .save() VS .create()



    # 겹치면 안되는게 또 뭐가 있을까 (어떤 값이 고유해야할까) - email, nickname 이 고유값이면 될것같다. (회원 구분 가능)
    def checkEmailDuplication(self, email):
        account_profile = self.__accountProfileRepository.findByEmail(email)
        print(f"account_profile: {account_profile}")
        return account_profile

    def checkNicknameDuplication(self, nickname):
        account_profile = self.__accountProfileRepository.findByNickname(nickname)
        return account_profile is not None



    # Id, 이메일로 전체 정보 조회
    def findProfileById(self, accountId):
        account_profile = self.__accountProfileRepository.findById(accountId)
        return account_profile

    def findProfileByEmail(self, email):
        account_profile = self.__accountProfileRepository.findByEmail(email)
        return account_profile



