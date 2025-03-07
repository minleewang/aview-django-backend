from django.http import JsonResponse
from rest_framework import viewsets

from av_db import settings

from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl

import requests


class AccountProfileController(viewsets.ViewSet):
    account_profile_service = AccountProfileServiceImpl.getInstance()

    def requestAccountProfile(self, email):
        """
        이메일을 기반으로 AccountProfile을 조회하고, 없으면 새로 생성
        """
        # 이메일을 통해 기존 프로필 조회
        account_profile = self.account_profile_service.findProfileByEmail(email)

        if account_profile is None:
            print(f"❌ {email}에 대한 프로필이 존재하지 않음. 새로 생성합니다.")

            # 가상의 기본값 설정
            default_nickname = email.split("@")[0]  # 이메일 아이디를 기본 닉네임으로 사용
            default_gender = None
            default_age_range = None
            default_birthyear = None
            default_login_type = "UNKNOWN"

            # 새 프로필 생성
            account_profile = self.account_profile_service.createAccountProfile(
                nickname=default_nickname,
                email=email,
                gender=default_gender,
                age_range=default_age_range,
                birthyear=default_birthyear,
                loginType=default_login_type
            )
            print(f"✅ 새 AccountProfile 생성 완료: ID={account_profile.id}")

        else:
            print(f"✅ 기존 AccountProfile 찾음: ID={account_profile.id}")

        return account_profile

    def social_login(self, request):
        """
        OAuth 토큰을 받아 사용자 정보를 조회 후 AccountProfile을 생성
        """
        token = request.GET.get("token")
        login_type = request.GET.get("loginType")  # 'KAKAO', 'GOOGLE', 'NAVER'

        if not token or not login_type:
            return JsonResponse({"error": "토큰 또는 로그인 타입이 누락되었습니다."}, status=400)

        user_info = self.get_user_info_from_oauth(token, login_type)

        if not user_info:
            return JsonResponse({"error": "OAuth 인증 실패"}, status=400)

        nickname = user_info.get("nickname")
        email = user_info.get("email")
        gender = user_info.get("gender")
        age_range = user_info.get("age_range")
        birthyear = user_info.get("birthyear")

        # AccountProfile 저장
        account_profile = self.account_profile_service.createAccountProfile(
            nickname, email, gender, age_range, birthyear, login_type
        )

        return JsonResponse({"message": "프로필 저장 성공", "accountProfileId": account_profile.id})

    def get_user_info_from_oauth(self, token, login_type):
        """
        외부 OAuth API를 호출하여 사용자 정보를 가져옴
        """
        url_map = {
            "KAKAO": settings.KAKAO['USER_INFO_REQUEST_URI'],
            "GOOGLE": settings.GOOGLE['USER_INFO_REQUEST_URI'],
            "NAVER": settings.NAVER['USER_INFO_REQUEST_URI'],
        }

        headers = {"Authorization": f"Bearer {token}"}
        url = url_map.get(login_type)

        if not url:
            return None

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return None

        data = response.json()

        # 각 플랫폼에 맞게 사용자 정보 변환
        if login_type == "KAKAO":
            return {
                "nickname": data["kakao_account"]["profile"]["nickname"],
                "email": data["kakao_account"]["email"],
                "gender": data["kakao_account"].get("gender"),
                "age_range": data["kakao_account"].get("age_range"),
                "birthyear": data["kakao_account"].get("birthyear"),
            }
        elif login_type == "GOOGLE":
            return {
                "nickname": data["name"],
                "email": data["email"],
                "gender": None,
                "age_range": None,
                "birthyear": None,
            }
        elif login_type == "NAVER":
            return {
                "nickname": data["response"]["nickname"],
                "email": data["response"]["email"],
                "gender": data["response"].get("gender"),
                "age_range": None,
                "birthyear": data["response"].get("birthyear"),
            }
        return None
