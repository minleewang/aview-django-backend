from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account_profile.controller.account_profile_controller import AccountProfileController


router = DefaultRouter()
router.register(r'account-profile', AccountProfileController, basename='account-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('create', AccountProfileController.as_view({'post':'createAccountProfile'}), name='카카오 사용자 정보 DB에 저장'),
    path('check-email', AccountProfileController.as_view({'get': 'check_email_duplication'}),
         name="Account Profile 이메일 중복 확인"),  # ✅ 이메일 중복 확인 추가
]