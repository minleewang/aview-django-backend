from django.http import JsonResponse
from rest_framework import viewsets

from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl

import requests


class AccountProfileController(viewsets.ViewSet):
    account_profile_service = AccountProfileServiceImpl.getInstance()

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
            "KAKAO": "https://kapi.kakao.com/v2/user/me",
            "GOOGLE": "https://www.googleapis.com/oauth2/v2/userinfo",
            "NAVER": "https://openapi.naver.com/v1/nid/me",
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
