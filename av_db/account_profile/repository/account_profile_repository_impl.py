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
        print(f"accountProfile: {gender}, {birthyear}, {age_range}")
        try:
            accountProfile = AccountProfile.objects.create(
                account=account,
                nickname=nickname,
                gender=gender or '',
                birthyear=birthyear or '',
                age_range=age_range or '')
            print(f"accountProfile: {gender}, {birthyear}, {age_range}")
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

    #email 찾기
    def findByEmail(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id = accountId)
            return accountProfile.account.email
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    #roletype 찾기
    def findByRoleType(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id = accountId)
            return accountProfile.account.roleType_id
        except Exception as e:
            print(f"Unexpected error, findByRoleType() : {str(e)}")
            return None

    #nickname 찾기
    def findByNickname(self, accountId):
        try:
            profileNickname=AccountProfile.objects.get(account_id = accountId)
            return profileNickname.nickname
        except ObjectDoesNotExist:
            print(f'No Account found for accountId: {accountId}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByNickname() : {str(e)}")
            return None

    #gender 찾기
    def findByGender(self, accountId):
        try:
            profileGender = AccountProfile.objects.get(account_id=accountId)
            return profileGender.gender
        except ObjectDoesNotExist:
            print(f'No Account found for accountId: {accountId}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByGender() : {str(e)}")
            return None

    #birthYar 찾기
    def findByBirthyear(self, accountId):
        try:
            profileBirth = AccountProfile.objects.get(account_id=accountId)
            return profileBirth.birthyear
        except ObjectDoesNotExist:
            print(f'No Account found for birthyear: {accountId}')  # 예외 발생 시 출력
            return None
        except Exception as e:
            print(f"Unexpected error, findByBirthyear() : {str(e)}")
            return None
