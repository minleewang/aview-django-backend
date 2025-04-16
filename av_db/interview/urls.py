from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview.controller.interview_controller import InterviewController

router = DefaultRouter()
router.register(r"interview", InterviewController, basename='interview')

urlpatterns = [
    path('', include(router.urls)),
    path('create',
         InterviewController.as_view({ 'post': 'requestCreateInterview' }),
         name='카트 생성 및 추가'),
    path('list',
         InterviewController.as_view({ 'post': 'requestListInterview' }),
         name='카트 리스트'),
    path('remove',
         InterviewController.as_view({ 'post': 'requestRemoveInterview' }),
         name='카트 제거'),
]