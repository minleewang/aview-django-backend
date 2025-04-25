from django.core.exceptions import ObjectDoesNotExist

from guest_account.repository.guest_account_repository_impl import GuestAccountRepositoryImpl
from guest_account.service.guest_account_service import GuestAccountService


class GuestAccountServiceImpl(GuestAccountService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__guestAccountRepository = GuestAccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # DB 생성
    def createGuestAccount(self, email, loginType):
        return self.__guestAccountRepository.save(email, loginType)

    # MyPage 회원정보 수정칸
    def findEmail(self, guestAccountId):
        try:
            guest_account = self.__guestAccountRepository.findById(guestAccountId)
            if guest_account:
                return guest_account.getEmail()  # account 객체에서 이메일 반환
            return None  # 이메일이 없으면 None 반환

        except ObjectDoesNotExist:
            return None