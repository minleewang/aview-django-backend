from django.core.exceptions import ObjectDoesNotExist

from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
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

    def createAccountProfile(self, accountId, nickname, gender, birthyear, age_range):
        print("profile 진입")
        if not nickname:
            nickname = "temporary"

        account = self.__accountRepository.findById(accountId)
        savedAccountProfile = self.__accountProfileRepository.save(account, nickname, gender, birthyear, age_range)
        if savedAccountProfile is not None:
            print(f"Profile 생성 성공: {savedAccountProfile}")
            return True

        print("Profile 생성 실패")
        return False

    def createAdminProfile(self, accountId, email):
        print("adminProfile 진입")

        account = self.__accountRepository.findById(accountId)
        saveAdminProfile = self.__accountProfileRepository.saveAdmin(account, email)
        if saveAdminProfile is not None:
            print(f"Profile 생성 성공: {saveAdminProfile}")
            return True

        print("adminProfile 생성 실패")
        return False

        # MyPage에서 정보 검색

    def findEmail(self, accountId):  # 얘는 account에서 참조해서 가져와야함
        try:
            accountProfile = self.__accountProfileRepository.findById(account_id=accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

    def findRoleType(self, accountId):  # 얘는 account에서 참조해서 가져와야함
        try:
            accountProfile = self.__accountProfileRepository.findByRoleType(account_id=accountId)
            return accountProfile  # account 객체에서 이메일 반환
        except ObjectDoesNotExist:
            return None

    def findNickname(self, accountId):
        try:
            accountProfile = self.__accountProfileRepository.findByNickname(id=accountId)
            if accountProfile:  #
                return accountProfile.getNickname()
            return None  # 이메일이 없으면 None 반환

        except ObjectDoesNotExist:
            return None

    def findGender(self, accountId):
        try:
            accountProfile = self.__accountProfileRepository.findByGender(id=accountId)
            if accountProfile:
                return accountProfile.getGender()  # account 객체에서 이메일 반환
            return None  # 이메일이 없으면 None 반환

        except ObjectDoesNotExist:
            return None

    def findBirthyear(self, accountId):
        try:
            accountProfile = self.__accountProfileRepository.findByBirthyear(id=accountId)
            if accountProfile:
                return accountProfile.getBirthyear()  # account 객체에서 이메일 반환
            return None  # 이메일이 없으면 None 반환

        except ObjectDoesNotExist:
            return None
