from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from account.entity.login_type import LoginType
from guest_account.entity.guest_account import GuestAccount
from guest_account.repository.guest_account_repository import GuestAccountRepository


class GuestAccountRepositoryImpl(GuestAccountRepository):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def save(self, new_guest_email, loginType):
        print(f"email: {new_guest_email}")
        loginType=loginType

        try:
            guest_account = GuestAccount.objects.create(
                email=new_guest_email,
                loginType=loginType,
            )
            print("완료")
            return guest_account

        except IntegrityError as e:
            print(
                f"email={new_guest_email}, loginType={loginType}")
            print(f"에러 내용: {e}")

            return None

    # DB에서 조회
    def findById(self, guestAccountId):
        print("여기까찌 옴")
        try:
            guest_account = GuestAccount.objects.get(id=guestAccountId)
            print(f"Account 찾음: {guest_account}")
            return guest_account
        except ObjectDoesNotExist:
            print(f"Account ID {guestAccountId} 존재하지 않음.")
            return None

    def findByEmail(self, email):
        try:
            print(f"{email}")
            return GuestAccount.objects.get(email=email)
        except ObjectDoesNotExist:
            print(f'No account found for email: {email}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def countEmail(self, guest_email):
        return GuestAccount.objects.filter(email__startswith=guest_email).count()
