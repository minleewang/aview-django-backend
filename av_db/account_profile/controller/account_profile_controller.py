from django.http import JsonResponse
from django.views.i18n import JavaScriptCatalog
from rest_framework import viewsets, status
from django.shortcuts import render

from account.entity.account import Account
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_service.service.redis_service_impl import RedisServiceImpl


class AccountProfileController(viewsets.ViewSet):
    __accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisServiceImpl.getInstance()

    def requestAccountProfileInfo(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")
        #data = request.data
        #nickname = data.get("nickname")
        #email = data.get("email")
        #loginType = data.get("loginType")

        # Token이 없으면 400_BAD_REQUEST 반환
        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        # Token이 있다면,
        try:
            # redis에서 userToken에 해당하는 accountId를 가져옴
            accountId = self.redisCacheService.getValueByKey(userToken)

            if not accountId:
                # redis에서 accountId를 찾지 못한 경우
                return JsonResponse({"error": "이메일을 찾을 수 없습니다.", "success": True}, status=status.HTTP_404_NOT_FOUND)

            # profile
            profileById = self.__accountProfileService.findProfileById(accountId)
            if profileById is None:  # 이메일 못찾은 경우
                return JsonResponse({"error": "회원 정보를 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({"Profile": profileById, "success": True}, status=status.HTTP_200_OK)


        # redis에서 찾은 accountId를 사용하여 이메일 찾기
            #foundEmail = self.__accountProfileService.findByEmail()
            foundEmail = self.redisCacheService.getValueByKey(userTocken)
            profileByEmail = self.accountProfileService.findProfileByEmail(foundEmail)

            if foundEmail is None:  # 이메일 못찾은 경우
                return JsonResponse({"error":"이메일을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({"email":"foundEmail", "success": True}, status=status.HTTP_200_OK)


        except Exception as e:
            # 예외 처리
            print(f"서버 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





"""""
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ ID로 계정 조회 (GET 요청)

    def get(self, request, accountId=None):
        if accountId:
            try:
                account = self.accountService.findAccountById(accountId)
                return Response({"id": account.id, "nickname": account.accountProfile.profile_nickname},
                                status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Account ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ 이메일로 계정 조회

    def get_by_email(self, request, email):
        try:
            account = self.accountService.findAccountByEmail(email)
            return Response({"id": account.id, "nickname": account.accountProfile.profile_nickname},
                                status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

            # ✅ 닉네임으로 계정 조회

    def get_by_nickname(self, request, nickname):
        try:
            account = self.accountService.findAccountByNickname(nickname)
            return Response({"id": account.id, "email": account.accountProfile.account_email},
                            status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

            # ✅ RoleType으로 계정 조회 (여러 개 가능)

    def get_by_role_type(self, request, roleType):
        try:
            accounts = self.accountService.findAccountByRoleType(roleType)
            account_list = [{"id": acc.id, "nickname": acc.accountProfile.profile_nickname} for acc in accounts]
            return Response({"accounts": account_list}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
"""""