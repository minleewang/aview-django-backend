from account.entity.account import Account
from account.entity.account_login_type import AccountLoginType
from account.entity.account_role_type import AccountRoleType
from account.entity.role_type import RoleType
from account.repository.account_repository import AccountRepository

from django.utils import timezone

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


    # 계정(객체) 생성
    def create(self, account_profile):
        print(f"account_profile: {account_profile}")
        defaultRoleType = AccountRoleType.objects.filter(roleType=RoleType.NORMAL).first()

        if not defaultRoleType:
            defaultRoleType = AccountRoleType(roleType=RoleType.NORMAL)
            defaultRoleType.save()
            print(f"Created new defaultRoleType: {defaultRoleType}")
        else:
            print(f"Found existing defaultRoleType : {defaultRoleType}")
        print(f"defaultRoleType: {defaultRoleType}")

        account = Account.objects.create(roleType=defaultRoleType, accountProfile=account_profile)
        print(f"account : {account}")

        account.save()
        return account



    # 계정 찾기
    def findById(self, accountId):
        account = Account.objects.get(id=accountId)
        print(f"findById result: {account}")
        return account

    def findByEmail(self, email):
        account = Account.objects.get(account_email=email)
        print(f"findByEmail result: {account}")
        return account

    def findByNickname(self, nickname):
        account = Account.objects.get(profile_nickname=nickname)
        print(f"findByNickname result: {account}")
        return account

    def findByRoleType(self, roleType):
        account = Account.objects.filter(roleType=roleType)  # 결과가 여러개여서 .filter() 사용
        print(f"findByNickname result: {account}")
        return account









    # 계정 탈퇴
    #def withdrawAccount(self, account, withdrawReason):
    #    role_type = AccountRoleType.objects.get(id=account.roleType_id)

    #    if role_type.roleType == "NORMAL":
    #        role_type.roleType = "BLACKLIST"
    #        role_type.save()

    #        account.roleType = role_type
    #        account.withdraw_reason = withdrawReason
    #        account.withdraw_at = timezone.now()
    #        account.save()
    #        print('계정 탈퇴 완료')
    #    else:
    #        raise ValueError('이미 탈퇴된 계정입니다')