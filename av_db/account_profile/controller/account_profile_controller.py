from django.http import JsonResponse
from rest_framework import viewsets, status

from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class AccountProfileController(viewsets.ViewSet):
    __accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()


    def requestInfo(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"error": "userToken이 없습니다.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Redis에서 userToken에 해당하는 accountId를 가져옴
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"accountId 나옴! : {accountId} ")

            if not accountId:
                # Redis에서 accountId를 찾지 못한 경우
                return JsonResponse({"error": "유효한 userToken이 아닙니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

            # accountId를 사용하여 이메일을 찾음
            foundEmail = self.__accountProfileService.findEmail(accountId)
            foundNickname = self.__accountProfileService.findNickname(accountId)
            foundGender = self.__accountProfileService.findGender(accountId)
            foundBirthyear = self.__accountProfileService.findBirthyear(accountId)

            #if foundEmail is None:
                # 이메일을 찾지 못한 경우
            #    return JsonResponse({"error": "이메일을 찾을 수 없습니다", "success": False}, status=status.HTTP_404_NOT_FOUND)

            # 이메일을 찾았으면 200 OK 응답
            return JsonResponse({
                "email": foundEmail,
                "gender": foundGender,
                "birthyear": foundBirthyear,
                "nickname" : foundNickname
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # 예외 처리
            print(f"서버 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
