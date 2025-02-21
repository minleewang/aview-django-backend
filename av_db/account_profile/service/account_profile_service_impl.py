from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
from account_profile.entity.account_profile_gender_type import AccountProfileGenderType
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

    def createAccountProfile(self, nickname, email, password, salt, gender, birthyear, account):
        genderType = AccountProfileGenderType.objects.get_or_create(gender_type=gender)
        gender = genderType[0]
        account_profile = AccountProfile.objects.create(
            nickname=nickname,
            email=email,
            password=password,
            salt=salt,
            gender=gender,
            birthyear=birthyear,
            account=account
        )
        return account_profile

    def checkEmailDuplication(self, email):
        account_profile = self.__accountProfileRepository.findByEmail(email)
        return account_profile is not None

    def checkNicknameDuplication(self, nickname):
        account_profile = self.__accountProfileRepository.findByNickname(nickname)
        return account_profile is not None

    def checkPasswordDuplication(self, email,password):
        account_profile = self.__accountProfileRepository.findByPassword(email,password)
        return account_profile

    def findProfileByEmail(self, email):
        account_profile = self.__accountProfileRepository.findByEmail(email)
        return account_profile

    def registerAccount(self, loginType, roleType, nickname, email, password, salt, gender, birthyear):
        account = self.__accountRepository.create(loginType, roleType)
        return self.__profileRepository.create(nickname, email, password, salt, gender, birthyear, account)