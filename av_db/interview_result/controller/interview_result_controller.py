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

    # 요약 생성
    @action(detail=False, methods=["post"])
    def requestInterviewSummary(self, request):
        try:
            data = request.data
            userToken = data.get("userToken")
            interviewId=data.get("interviewId")

            accountId = self.redisCacheService.getValueByKey(userToken)
            context = {
                "userToken": userToken,
                "topic": data.get("jobCategory"),
                "experienceLevel": data.get("experienceLevel"),
                "projectExperience": data.get("projectExperience"),
                "academicBackground": data.get("academicBackground"),
                "interviewTechStack": data.get("interviewTechStack"),
            }

            questions, answers = self.interviewResultService.getFullQAList(interviewId)

            if not questions or not answers:
                raise Exception("질문/답변 복원 실패")

            # FastAPI 전송용 payload 생성
            payload = {
                "session_id": f"interview-{interviewId}",
                "context": context,
                "questions": questions,
                "answers": answers
            }

            print(f"📡 FastAPI 요청: {payload}")
            response = HttpClient.postToAI("/interview/question/end_interview", payload)

            if not response or not response.get("summary"):
                raise Exception("FastAPI 응답 실패")

            summary = response["summary"]

            # 결과 저장
            self.interviewResultService.saveInterviewResult(accountId, userToken, summary, questions, answers)

            return JsonResponse({
                "message": "면접 결과 요약 및 저장 완료",
                "summary": summary,
                "success": True
            }, status=200)

        except Exception as e:
            print(f"❌ requestInterviewSummary 오류: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    def getInterviewResult(self, request):
        userToken = request.data.get('userToken')
        accountId = self.redisCacheService.getValueByKey(userToken)
        interviewResultList = self.interviewResultService.getInterviewResult(accountId)
        result_list = list(interviewResultList)
        print(f"결과:{result_list}")
        return JsonResponse({'interviewResultList': result_list}, status=status.HTTP_200_OK)