from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview_question.controller.interview_question_controller import InterviewQuestionController

router = DefaultRouter()
router.register(r"interview-question", InterviewQuestionController, basename='interview-question')

urlpatterns = [
    path('', include(router.urls)),
    path('save-bulk',
         InterviewQuestionController.as_view({ 'post': 'requstSaveBulkInterviewQuestion' }),
         name='생성한 질문 리스트 저장'),
    path('list',
         InterviewQuestionController.as_view({ 'post': 'requestListInterviewQuestion' }),
         name='질문 목록 조회'),
]