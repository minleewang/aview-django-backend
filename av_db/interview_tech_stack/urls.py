from django.urls import path, include
from rest_framework.routers import DefaultRouter

from interview_tech_stack.controller.interview_tech_stack_controller import InterviewTechStackController

router = DefaultRouter()
router.register(r"interview_tech_stack", InterviewTechStackController, basename='interview_tech_stack')

urlpatterns = [
    path('', include(router.urls)),
    path('list',
         InterviewTechStackController.as_view({ 'get': 'requestListInterviewTechStack' }),
         name='기술 스텍 리스트 저장'),
]