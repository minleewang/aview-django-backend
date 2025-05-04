from django.db import transaction
from django.shortcuts import render

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from interview_result.service.interview_result_service_impl import InterviewResultServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from utility.http_client import HttpClient


class InterviewResultController(viewsets.ViewSet):
    interviewResultService = InterviewResultServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def reqeustEndInterview(self, request):
        try:
            postRequest = request.data
            print(f"{postRequest}")

            userToken = postRequest.get("userToken")
            interviewId = postRequest.get("interviewId")
            questionId = postRequest.get("questionId")
            answerText = postRequest.get("answerText")
            jobCategory = postRequest.get("jobCategory")
            experienceLevel = postRequest.get("experienceLevel")
            projectExperience = postRequest.get("projectExperience")
            academicBackground = postRequest.get("academicBackground")
            interviewTechStack = postRequest.get("interviewTechStack")

            if not userToken or not interviewId or not questionId or not answerText:
                return JsonResponse({
                    "error": "필수 값이 누락되었습니다",
                    "success": False
                }, status=status.HTTP_400_BAD_REQUEST)

            payload = {
                "userToken": userToken,
                "interviewId": interviewId,
                "questionId": questionId,
                "answerText": answerText,
                "topic": jobCategory,
                "experienceLevel": experienceLevel,
                "projectExperience": projectExperience,
                "academicBackground": academicBackground,
                "interviewTechStack": interviewTechStack,
            }
            print(f"이것:{payload}")

            print(f"\n📤 [Service] FastAPI로 면접 종료 요청 전송: {payload}")
            result = HttpClient.postToAI(
                "/interview/question/end_interview",
                data=payload
            )

            if not result:
                raise Exception("FastAPI에서 실패 응답 반환 또는 연결 실패")

            print(f"✅ [Service] FastAPI 응답 수신 완료")

            return JsonResponse({
                "message": "면접 종료 요청이 완료되었습니다.",
                "result": result,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ 면접 종료 처리 실패: {e}")
            return JsonResponse({
                "error": "서버 오류 발생",
                "success": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #def saveInterviewResult(self, request):
     #   try:
            #scoreResultList = request.data.get('scoreResultList') # 질문, 답변, 의도, 점수+피드백

      #      userToken = request.data.get('userToken')
       #     accountId = self.redisCacheService.getValueByKey(userToken)

#            self.interviewResultService.saveInterviewResult(accountId)

 #           return Response(True, status=status.HTTP_200_OK)

  #      except Exception as e :
   #         print('interview result 저장중 error: ', e)

    def getInterviewResult(self, request):
        print(f"{request}")
        userToken = request.data.get('userToken')
        accountId = self.redisCacheService.getValueByKey(userToken)
        interviewResultList = self.interviewResultService.getInterviewResult(accountId)
        result_list = list(interviewResultList)
        print(f"{result_list}")
        return JsonResponse({'interviewResultList': result_list}, status=status.HTTP_200_OK)