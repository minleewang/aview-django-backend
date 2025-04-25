from django.db import transaction
from django.shortcuts import render

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from interview.service.interview_service_impl import InterviewServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl
from utility.http_client import HttpClient


class InterviewController(viewsets.ViewSet):
    redisCacheService = RedisCacheServiceImpl.getInstance()
    interviewService = InterviewServiceImpl.getInstance()

    def requestCreateInterview(self, request):
        postRequest = request.data
        print(f"postRequest: {postRequest}")

        userToken = postRequest.get("userToken")
        jobCategory = postRequest.get("jobCategory")
        experienceLevel = postRequest.get("experienceLevel")
        projectExperience = postRequest.get("projectExperience")
        academicBackground = postRequest.get("academicBackground")
        interviewTechStack = postRequest.get("interviewTechStack")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        if not jobCategory or not experienceLevel or not projectExperience or not academicBackground or not interviewTechStack:
            return JsonResponse({"error": "jobCategory, experienceLevel, projectExperience, academicBackground, interviewTechStack이 필요합니다", "success": False},
                                status=status.HTTP_400_BAD_REQUEST)

        print(f"userToken 획득")

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"accountId 찾기: {accountId}")

            with transaction.atomic():  # ✅ 트랜잭션 블록 시작
                createdInterview = self.interviewService.createInterview(
                    accountId, jobCategory, experienceLevel, projectExperience, academicBackground, interviewTechStack  # 지금 accountId가 안옴
                )
                print(f"createdInterview : {createdInterview}")

                if createdInterview is None:
                    raise Exception("면접 생성 실패")

                payload = {
                    "userToken": userToken,
                    "interviewId": str(createdInterview.id),
                    "topic": createdInterview.topic,
                    "experienceLevel": createdInterview.experience_level,
                    "projectExperience": createdInterview.project_experience,
                    "academicBackground": createdInterview.academic_background,
                    "interviewTechStack": createdInterview.interview_tech_stack
                }
                print(f" 아 드디어 여기까지 옴: payload {payload}")

                response = HttpClient.postToAI("/interview/question/generate", payload)
                print(f"FastAPI Response: {response}")

                if not response:
                    raise Exception("FastAPI 질문 생성 실패")

                question = response["questions"]
                questionId = self.interviewService.saveQuestion(createdInterview.id, question)

                if questionId is None:
                    raise Exception("질문 저장 실패")

            return JsonResponse({
                "message": "면접 정보가 추가되었습니다.",
                "interviewId": createdInterview.id,
                "questionId": questionId,
                "question": question,
                "success": True
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ 면접 생성 트랜잭션 실패: {e}")
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

    @action(detail=False, methods=["post"])
    def requestCreateAnswer(self, request):
        postRequest = request.data
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        questionId = postRequest.get("questionId")
        answerText = postRequest.get("answerText")

        if not userToken or not interviewId or not questionId or not answerText:
            return JsonResponse({
                "error": "userToken, interviewId, questionId, answerText 모두 필요합니다.",
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            accountId = self.redisCacheService.getValueByKey(userToken)

            with transaction.atomic():
                result = self.interviewService.saveAnswer(
                    accountId=accountId,
                    interviewId=interviewId,
                    questionId=questionId,
                    answerText=answerText
                )

                if not result:
                    raise Exception("답변 저장 실패")

            return JsonResponse({"message": "답변 저장 완료", "success": True})

        except Exception as e:
            print(f"[Error] requestCreateAnswer: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)

    @action(detail=False, methods=["post"])
    def requestFollowUpQuestion(self, request):
        # POST 요청으로부터 데이터 파싱
        postRequest = request.data
        userToken = postRequest.get("userToken")
        interviewId = postRequest.get("interviewId")
        questionId = postRequest.get("questionId")
        answerText = postRequest.get("answerText")

        # 필수 값이 누락된 경우 400 Bad Request 반환
        if not userToken or not interviewId or not questionId or not answerText:
            return JsonResponse({
                "error": "userToken, interviewId, questionId, answerText 모두 필요합니다.",
                "success": False
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # FastAPI로 전송할 payload 구성
            payload = {
                "userToken": userToken,
                "interviewId": interviewId,
                "questionId": questionId,
                "answerText": answerText
            }

            # FastAPI에 후속 질문 요청 API 호출
            response = HttpClient.postToAI("/interview/question/generate-after-answer", payload)
            print(f"[FastAPI] Follow-up response: {response}")

            # FastAPI 응답이 없으면 에러 처리
            if not response:
                raise Exception("FastAPI 질문 생성 실패")

            # 정상 응답일 경우 클라이언트에 응답 전달
            return JsonResponse(response, status=200)

        except Exception as e:
            # 예외 발생 시 로그 출력 및 에러 응답 반환
            print(f"[Error] requestFollowUpQuestion: {e}")
            return JsonResponse({"error": str(e), "success": False}, status=500)
