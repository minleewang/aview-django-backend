from django.http import JsonResponse
from rest_framework import viewsets

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
import jwt
import datetime
from django.conf import settings

class AccountController(viewsets.ViewSet):
    account_service = AccountServiceImpl.getInstance()
    account_profile_service = AccountProfileServiceImpl.getInstance()

    def login(self, request):
        """
        AccountProfile 정보를 기반으로 Account 생성 및 로그인 처리
        """
        email = request.GET.get("email")
        nickname = request.GET.get("nickname")
        login_type = request.GET.get("loginType")

        if not email or not nickname or not login_type:
            return JsonResponse({"error": "필수 정보가 누락되었습니다."}, status=400)

        # AccountProfile 조회
        account_profile = self.account_profile_service.findProfileByEmail(email)

        if not account_profile:
            return JsonResponse({"error": "AccountProfile이 존재하지 않습니다."}, status=400)

        # Account 존재 여부 확인
        try:
            account = self.account_service.findAccountByEmail(email)
        except:
            # 존재하지 않으면 Account 생성
            account = self.account_service.createAccount(
                nickname=nickname,
                email=email,
                loginType=login_type
            )

        # JWT 토큰 발급
        token = self.generate_jwt(account.id)

        return JsonResponse({"message": "로그인 성공", "token": token})

    def generate_jwt(self, account_id):
        """
        JWT 토큰 생성 (예외 처리 포함)
        """
        try:
            # ✅ 만료 시간 설정 (1일 후 만료)
            exp_time = datetime.datetime.now() + datetime.timedelta(days=1)

            payload = {
                "account_id": account_id,
                "exp": exp_time,  # 만료 시간
                "iat": datetime.datetime.now()  # 발급 시간
            }

            # ✅ settings.SECRET_KEY 확인 후 JWT 생성
            if not hasattr(settings, "SECRET_KEY") or not settings.SECRET_KEY:
                raise ValueError("Django settings에 SECRET_KEY가 설정되지 않았습니다.")

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            # ✅ JWT가 bytes로 반환될 경우 str로 변환
            if isinstance(token, bytes):
                token = token.decode("utf-8")

            return token

        except Exception as e:
            print(f"JWT 생성 중 오류 발생: {str(e)}")
            return None  # 오류 발생 시 None 반환