from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


from django.utils import timezone

from account_profile.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository import AccountProfileRepository
from account_profile.entity.account_profile_gender_type import AccountProfileGenderType

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

    def create(self, nickname, email, password, salt, gender, birthyear, account):
        genderType = AccountProfileGenderType.objects.get_or_create(gender_type=gender)
        gender = genderType[0]
        account_profile = AccountProfile.objects.create(
            nickname=nickname,
            email=email,
            password=password,
            salt=salt,
            gender=gender,
            birthyear=birthyear,
            account=account
        )
        return account_profile

    def save(self, account, nickname):
        try:
            accountProfile = AccountProfile.objects.create(account=account, nickname=nickname)
            return accountProfile

        except IntegrityError:
            raise IntegrityError(f"Nickname '{nickname}' 이미 존재함.")

    def findByAccount(self, account):
        try:
            # 주어진 Account 객체에 해당하는 AccountProfile을 조회
            return AccountProfile.objects.get(account=account)
        except AccountProfile.DoesNotExist:
            # 만약 해당하는 AccountProfile이 없으면 None을 반환
            return None

    def findById(self, accountId):
        try:
            accountProfile = AccountProfile.objects.get(account_id=accountId)
            return accountProfile
        except AccountProfile.DoesNotExist:
            print('accountId와 일치하는 계정이 없습니다')
            return None
        except Exception as e:
            print(f"accountId로 계정 찾는 중 에러 발생: {e}")
            return None

    def findByPassword(self, email,password):
        try:
            email = AccountProfile.objects.get(email=email)
            return email.password == password
        except email.DoesNotExist:
            print('password가 일치하지 않습니다.')
            return None
        except Exception as e:
            print(f"password로 계정 찾는 중 에러 발생: {e}")
            return None

    def findByEmail(self, email):
        try:
            accountProfile = AccountProfile.objects.get(email=email)
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

    def findGenderTypeByGenderId(self, genderId):
        try:
            genderType = AccountProfileGenderType.objects.get(id=genderId)
            return genderType
        except AccountProfileGenderType.DoesNotExist:
            print('genderId와 일치하는 genderType이 없습니다')
            return None
        except Exception as e:
            print(f"genderId로 genderType 찾는 중 에러 발생: {e}")
            return None

    # 접속시간 기록을 위한 추가
    def updateLastLogin(self, profile):
        try:
            profile.last_login = timezone.now() + timezone.timedelta(hours=9)
            profile.save()
        except Exception as e:
            print(f"최근 접속시간 업데이트 중 에러 발생: {e}")
            return None

    def update_login_history(self, profile):
        try:
            login_history = LoginHistory.objects.create(account_id=profile.account.id)
            return login_history
        except Exception as e:
            print(f"로그인 기록 생성 중 에러 발생: {e}")
            return None