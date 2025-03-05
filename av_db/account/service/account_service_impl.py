
from django.core.exceptions import ObjectDoesNotExist

from account.repository.account_repository_impl import AccountRepositoryImpl
from account.service.account_service import AccountService
from account_profile.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl


class AccountServiceImpl(AccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            #cls.__instance.__accountProfileRepository = AccountProfileRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    # Account 생성
    def createAccount(self, nickname, email, loginType):
        # nickname, email, loginType은 account_profile의 db에서 오는 정보
        # 1) account_profile에서 사용자 정보 가져오기
        try:
            account_profile = AccountProfile.objects.get(
                profile_nickname=nickname,
                account_email=email,
                loginType=loginType
            )
            # 2) Account 객체 생성하기 (객체생성은 .create()로 repositoryimpl에서 구현)
            account = self.__accountRepository.create(account_profile)
            # self.__accountRepository.create(roleType=roleType, accountProfile=account_profile)

            return account

        except AccountProfile.ObjectDoesNotExist:
            # 만약 해당 프로필이 없으면 오류 처리
            raise ValueError("AccountProfile 정보가 존재하지 않습니다.")




    # Account DB에서 계정 정보 찾기    (email, roleType, nickname)
    # id로 전체 계정을 조회하기
    def findAccountById(self, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            return account
        except ObjectDoesNotExist:
            error_message = f"accountId={accountId}번째 계정이 존재하지 않습니다."
            print(f"ERROR: {error_message}")
            raise ValueError(error_message)
    # 이메일로 전체 계정 조회
    def findAccountByEmail(self, email):
        try:
            account = self.__accountRepository.findByEmail(email)
            return account
        except ObjectDoesNotExist:
            error_message = f"email={email}을 가진 계정이 존재하지 않습니다."
            print(f"ERROR: {error_message}")
            raise ValueError(error_message)
    # 닉네임으로 전체 계정 조회
    def findAccountByNickname(self, nickname):
        try:
            account = self.__accountRepository.findByNickname(nickname)
            return account
        except ObjectDoesNotExist:
            error_message = f"nickname={nickname}을 가진 계정이 존재하지 않습니다."
            print(f"ERROR: {error_message}")
            raise ValueError(error_message)
    # roleType별 계정 분류 (결과 여러개 나옴)
    def findAccountByRoleType(self, roleType):
        try:
            account = self.__accountRepository.findByRoleType(roleType)
            for num in account:
                print(num)
            return account
        except ObjectDoesNotExist:
            error_message = f"roleType={roleType}을 가진 계정(들)이 존재하지 않습니다."
            print(f"ERROR: {error_message}")
            raise ValueError(error_message)
        # roleType별로 분리된 DB 혹은 결과에서 email, nickname을 검색하게 할 수 있나?




    # 계정 삭제
    #def withdrawAccount(self, accountId, withdrawReason):
    #    account = self.__accountRepository.findById(accountId)
    #    try:
    #        self.__accountRepository.withdrawAccount(account, withdrawReason)
    #        return True
    #    except Exception as e:
    #        print(f"withdraw_account error: {e}")
    #        return False
