import hashlib
import random
import string

from rest_framework import viewsets, status
from rest_framework.response import Response

from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.entity.account_profile import AccountProfile
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from account.serializer.account_serializer import AccountSerializer
from account.service.account_service_impl import AccountServiceImpl
from redis_service.service.redis_service_impl import RedisServiceImpl


class AccountController(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    accountProfileRepository = AccountProfileRepositoryImpl.getInstance()
    accountRepository = AccountRepositoryImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()

    def checkEmailDuplication(self, request):
        print("checkEmailDuplication()")

        try:
            print(f"request.data: {request.data}")
            email = request.data.get("email")
            print(f"email: {email}")
            isDuplicate = self.accountService.checkEmailDuplication(email)
            print(f"isDuplicate: {isDuplicate}")

            return Response(
                {
                    "isDuplicate": isDuplicate,
                    "message": (
                        "Email이 이미 존재" if isDuplicate else "Email 사용 가능"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("이메일 중복 체크 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def checkNicknameDuplication(self, request):
        print("checkNicknameDuplication()")

        try:
            nickname = request.data.get("newNickname")
            print(f"nickname: {nickname}")
            isDuplicate = self.accountService.checkNicknameDuplication(nickname)

            return Response(
                {
                    "isDuplicate": isDuplicate,
                    "message": (
                        "Nickname이 이미 존재" if isDuplicate else "Nickname 사용 가능"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("닉네임 중복 체크 중 에러 발생:", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def registerAccountProfile(self, request):
        try:
            nickname = request.data.get("nickname")
            email = request.data.get("email")
            password = request.data.get("password")
            gender = request.data.get("gender")  # 성별 추가
            birthyear = request.data.get("birthyear")  # 생년월일 추가
            randomString = string.ascii_letters + string.digits + string.punctuation
            salt = ''.join(random.choice(randomString) for _ in range(16))
            encodedPassword = salt.encode("utf-8") + password.encode("utf-8")
            hashedPassword = hashlib.sha256(encodedPassword)
            password = hashedPassword.hexdigest()
            loginType = request.data.get("loginType")

            if loginType == "NORMAL":
                account = self.accountService.registerAccount(
                    loginType=loginType,
                    roleType="NORMAL",
                    nickname=nickname,
                    email=email,
                    password=password,
                    salt=salt,
                    gender=gender,
                    birthyear=birthyear,
                )
            elif email == "Ai-View@kakao.com":
                account = self.accountService.registerAccount(
                    loginType=loginType,
                    roleType="ADMIN",
                    nickname=nickname,
                    email=email,
                    password=None,
                    salt=None,
                    gender=gender,
                    birthyear=birthyear,
                )
            else:
                account = self.accountService.registerAccount(
                    loginType=loginType,
                    roleType="NORMAL",
                    nickname=nickname,
                    email=email,
                    password=None,
                    salt=None,
                    gender=gender,
                    birthyear=birthyear,
                )

            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("계정 생성 중 에러 발생:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def getNickname(self, request):
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)
        account_profile = self.accountProfileRepository.findByEmail(email)
        if account_profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        nickname = account_profile.nickname
        return Response(nickname, status=status.HTTP_200_OK)

    def getGender(self, request):
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)
        account_profile = self.accountProfileRepository.findByEmail(email)
        if account_profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        genderId = account_profile.gender_id
        accountProfileGenderType = self.accountProfileRepository.findGenderTypeByGenderId(genderId)
        genderType = accountProfileGenderType.gender_type
        return Response(genderType, status=status.HTTP_200_OK)

    def getBirthyear(self, request):
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_200_OK)
        account_profile = self.accountProfileRepository.findByEmail(email)
        if account_profile is None:
            return Response(
                {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )  # 에러 처리 추가
        birthyear = account_profile.birthyear
        return Response(birthyear, status=status.HTTP_200_OK)

    def checkPassword(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            profile = AccountProfile.objects.get(email=email)
            salt = profile.salt
            hashed = salt.encode('utf-8') + password.encode("utf-8")
            hash_obj = hashlib.sha256(hashed)
            password = hash_obj.hexdigest()

            isDuplicate = self.accountService.checkPasswordDuplication(email, password)

            return Response({'isDuplicate': isDuplicate, 'message': 'password가 이미 존재' \
                if isDuplicate else 'password 사용 가능'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("password 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def modifyNickname(self,request):
        email = request.data.get('email')
        newNickname = request.data.get('newNickname')

        if not email:
            return Response(None,status=status.HTTP_200_OK)
        account_profile = self.accountProfileRepository.findByEmail(email)

        if account_profile is None:
            return Response(
                {"error":"Profile not found"},status=status.HTTP_400_BAD_REQUEST
            )
        account_profile.nickname = newNickname
        account_profile.save()
        print(f"nickname: {account_profile.nickname}")
        return Response(account_profile.nickname,status=status.HTTP_200_OK)

    def modifyPassword(self,request):
        email = request.data.get('email')
        newPassword = request.data.get('newPassword')
        profile = AccountProfile.objects.get(email=email)
        salt = profile.salt
        print(salt)
        hashed = salt.encode('utf-8') + newPassword.encode("utf-8")
        hash_obj = hashlib.sha256(hashed)
        newpassword1 = hash_obj.hexdigest()

        if not email:
            return Response(None,status=status.HTTP_200_OK)
        account_profile = self.accountProfileRepository.findByEmail(email)

        if account_profile is None:
            return Response(
                {"error":"Profile not found"},status=status.HTTP_400_BAD_REQUEST
            )
        account_profile.password = newpassword1
        account_profile.save()
        print(f"newPassword: {account_profile.password}")
        return Response(account_profile.password, status=status.HTTP_200_OK)

    def getAccountProfile(self, request):
        email = request.data.get("email")
        if not email:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        account_profile = self.accountService.findAccountProfileByEmail(email)
        if account_profile is None:
            return Response({'error': 'AccountProfile not found'}, status=status.HTTP_404_NOT_FOUND)

        # 필요한 필드만 반환, gender 필드를 문자열로 변환
        account_profile_data = {
            'email': account_profile.email,
            'nickname': account_profile.nickname,
            'gender': str(account_profile.gender),  # 문자열로 변환
            'birthyear': account_profile.birthyear
        }
        return Response(account_profile_data, status=status.HTTP_200_OK)

