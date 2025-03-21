from django.db import IntegrityError

from account_profile.entity.account_profile import AccountProfile
from account_profile.entity.admin_profile import AdminProfile
from account_profile.repository.account_profile_repository import AccountProfileRepository


class AccountProfileRepositoryImpl(AccountProfileRepository):
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

    def save(self, account, nickname, gender, birthyear, age_range):
        try:
            accountProfile = AccountProfile.objects.create(
                account=account,
                nickname=nickname,
                gender=gender,
                birthyear=birthyear,
                age_range=age_range)
            return accountProfile

        except IntegrityError:
            raise IntegrityError(f"Nickname '{nickname}' 이미 존재함.")


    def saveAdmin(self, account, email):
        print(f"account: {account}")
        adminProfile = AdminProfile(account=account, email=email)
        print(f"야 찍히냐?")

        adminProfile.save()
        print(f"account: {adminProfile}")

        return adminProfile

    def findByAccount(self, account):
        try:
            # 주어진 Account 객체에 해당하는 AccountProfile을 조회
            return AccountProfile.objects.get(account=account)
        except AccountProfile.DoesNotExist:
            # 만약 해당하는 AccountProfile이 없으면 None을 반환
            return None