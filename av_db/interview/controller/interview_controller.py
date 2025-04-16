from django.shortcuts import render

from django.http import JsonResponse
from rest_framework import viewsets, status

from interview.service.interview_service_impl import InterviewServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class InterviewController(viewsets.ViewSet):
    redisCacheService = RedisCacheServiceImpl.getInstance()
    interviewService = InterviewServiceImpl.getInstance()

    def requestCreateInterview(self, request):
        postRequest = request.data
        print(f"postRequest: {postRequest}")

        userToken = postRequest.get("userToken")
        jobCategory = postRequest.get("jobCategory")
        experienceLevel = postRequest.get("experienceLevel")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        if not jobCategory or not experienceLevel:
            return JsonResponse({"error": "jobCategory와 experienceLevel이 필요합니다", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        print(f"userToken 획득")

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"accountId 찾기: {accountId}")

            createdInterview = self.interviewService.createInterview(
                accountId, jobCategory, experienceLevel
            )
            print(f"createdInterview: {createdInterview}")
            if createdInterview is not None:
                return JsonResponse({
                    "message": "면접 정보가 추가되었습니다.",
                    "interviewId": createdInterview.id,
                    "success": True
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"면접 정보 생성 중 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestListInterview(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")

        page = postRequest.get("page", 1)
        perPage = postRequest.get("perPage", 10)

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)

            interviewList, totalItems = self.interviewService.listInterview(accountId, page, perPage)

            return JsonResponse({
                "interviewList": interviewList,
                "totalItems": totalItems,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"면접 정보 조회 중 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestRemoveInterview(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("id")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            result = self.interviewService.removeInterview(accountId, interviewId)

            if result["success"]:
                return JsonResponse(result, status=status.HTTP_200_OK)
            else:
                return JsonResponse(result, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"면접 정보 제거 중 오류 발생: {e}")
            return JsonResponse({"error": "서버 내부 오류", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
