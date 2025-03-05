from tkinter.font import names

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.controller.account_controller import AccountController

router = DefaultRouter()
router.register(r'account', AccountController, basename='account')

urlpatterns = [
    path('', include(router.urls)),
    path('login', AccountController.as_view({'post': 'login'}), name="Account 로그인"),  # ✅ 로그인 엔드포인트 추가
]