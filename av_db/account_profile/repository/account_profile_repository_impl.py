from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from account_profile.entity.account_profile import AccountProfile
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

    def findByAccount(self, account): # 객체 하나로 전체 정보 가져오기
        try:
            # 주어진 Account 객체에 해당하는 AccountProfile을 조회
            return AccountProfile.objects.get(account=account)
        except AccountProfile.DoesNotExist:
            # 만약 해당하는 AccountProfile이 없으면 None을 반환
            return None

    def findByEmail(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id = accountId)
            return accountProfile.account.email
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def findByRoleType(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id = accountId)
            return accountProfile.account.roleType_id
        except Exception as e:
            print(f"Unexpected error, findByRoleType() : {str(e)}")
            return None

    def findByNickname(self, nickname):
        try:
            print(f"{nickname}")
            return AccountProfile.objects.get(nickname=nickname)
        except ObjectDoesNotExist:
            print(f'No Account found for nickname: {nickname}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByNickname() : {str(e)}")
            return None

    def findByGender(self, gender):
        try:
            print(f"{gender}")
            return AccountProfile.objects.get(gender=gender)
        except ObjectDoesNotExist:
            print(f'No Account found for gender: {gender}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByGender() : {str(e)}")
            return None

    def findByBirthyear(self, birthyear):
        try:
            print(f"{birthyear}")
            return AccountProfile.objects.get(birthyear=birthyear)
        except ObjectDoesNotExist:
            print(f'No Account found for birthyear: {birthyear}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByBirthyear() : {str(e)}")
            return None
