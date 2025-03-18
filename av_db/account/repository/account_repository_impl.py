from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from account.entity.account_login_type import AccountLoginType
from account.entity.account import Account
from account.entity.account_role_type import AccountRoleType
from account.entity.role_type import RoleType
from account.repository.account_repository import AccountRepository


class AccountRepositoryImpl(AccountRepository):
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

    def save(self, email, loginType):
        print(f"email: {email}")
        defaultRoleType = AccountRoleType.objects.filter(roleType=RoleType.NORMAL).first()
        loginTypeInstance, created = AccountLoginType.objects.get_or_create(loginType=loginType)

        # 만약 기본 역할이 없다면, 새로 생성
        if not defaultRoleType:
            defaultRoleType = AccountRoleType(roleType=RoleType.NORMAL)
            defaultRoleType.save()
            print(f"Created new defaultRoleType: {defaultRoleType}")
        else:
            print(f"Found existing defaultRoleType: {defaultRoleType}")

        print(f"defaultRoleType: {defaultRoleType}")

        try:
            account = Account.objects.create(

                email=email,
                loginType=loginTypeInstance,
                roleType=defaultRoleType,
            )
            print("완료")
            return account

        except IntegrityError as e:

            print(
                f"email={email}, roleType={defaultRoleType}, loginType={loginType}")

            print(f"에러 내용: {e}")

            return None
            # raise IntegrityError(f"Nickname '{nickname}' 이미 존재함.")

    def saveAdmin(self, email):
        print(f"email: {email}")
        defaultRoleType = AccountRoleType.objects.filter(role_type=RoleType.ADMIN).first()

        # 만약 기본 역할이 없다면, 새로 생성
        if not defaultRoleType:
            defaultRoleType = AccountRoleType(role_type=RoleType.ADMIN)
            defaultRoleType.save()
            print(f"Created new defaultRoleType: {defaultRoleType}")
        else:
            print(f"Found existing defaultRoleType: {defaultRoleType}")

        print(f"defaultRoleType: {defaultRoleType}")

        account = Account(email=email, role_type=defaultRoleType)
        print(f"account: {account}")

        account.save()
        return account

    def findById(self, accountId):
        try:
            return Account.objects.get(id=accountId)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Account ID {accountId} 존재하지 않음.")

    def findByEmail(self, email):
        try:
            print(f"{email}")
            return Account.objects.get(email=email)
        except ObjectDoesNotExist:
            print(f'No account found for email: {email}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def deleteAccount(self, accountId: int) -> bool:
        try:
            account = Account.objects.get(id=accountId)
            account.delete()
            return True
        except Account.DoesNotExist:
            return False
