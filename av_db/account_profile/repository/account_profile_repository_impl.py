from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone

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



    def save(self, nickname, email, gender, age_range, birthyear,loginType):
        try:
            accountProfile = AccountProfile.objects.create(

                nickname=nickname,
                email=email,
                gender=gender,
                age_range=age_range,
                birthyear=birthyear,
                loginType=loginType
            )
            return accountProfile

        except IntegrityError:
            print(f"profile_nickname={nickname},account_email={email}, gender={gender}, age_range={age_range}, birthyear={birthyear}, loginType={loginType}")
            raise IntegrityError(f"account_profile에 정보를 저장할 수 없음")
            #raise IntegrityError(f"Nickname '{nickname}' 이미 존재함.")



    # 검색 find 기능 구현
    def findById(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(id=accountId)
            return accountProfile
        except AccountProfile.DoesNotExist:
            print(f"id로 profile 찾을 수 없음: {accountId}")
            return None
        except Exception as e:
            print(f"id 중복 검사 중 에러 발생: {e}")
            return None

    def findByEmail(self, email):
        try:
            accountProfile = AccountProfile.objects.get(email=email)
            print(f"찾은 AccountProfile: {accountProfile}")  # 디버깅용 로그 추가
            return accountProfile
        except AccountProfile.DoesNotExist:
            print(f"email로 profile 찾을 수 없음: {email}")
            return None
        except Exception as e:
            print(f"email 중복 검사 중 에러 발생: {e}")
            return None

    def findByNickname(self, nickname):
        try:
            accountProfile = AccountProfile.objects.get(nickname=nickname)
            return accountProfile
        except AccountProfile.DoesNotExist:
            print(f"nickname으로 profile 찾을 수 없음: {nickname}")
            return None
        except Exception as e:
            print(f"nickname 중복 검사 중 에러 발생: {e}")
            return None

