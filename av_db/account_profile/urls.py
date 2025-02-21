from tkinter.font import names

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account_profile.controller.account_profile_controller import AccountController

router = DefaultRouter()
router.register(r'account-profile', AccountController, basename='account-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('email-duplication-check',
         AccountController.as_view({'post': 'checkEmailDuplication'}), name='account-email-duplication-check'),
    path('nickname-duplication-check',
         AccountController.as_view({'post': 'checkNicknameDuplication'}), name='account-nickname-duplication-check'),
    path('register', AccountController.as_view({'post': 'registerAccountProfile'}), name='register-account'),
    path('nickname', AccountController.as_view({'post': 'getNickname'}), name='nickname-account'),
    path('gender', AccountController.as_view({'post': 'getGender'}), name='gender-account'),
    path('birthyear', AccountController.as_view({'post': 'getBirthyear'}), name='birthyear-account'),
    path('check-password', AccountController.as_view({'post': 'checkPassword'}), name='normal-login-check-account'),
    path('modify-nickname',AccountController.as_view({'post':'modifyNickname'}),name='account-modify-nickname'),
    path('modify-password',AccountController.as_view({'post':'modifyPassword'}),name='account-modify-password'),
    path('get-account-profile',AccountController.as_view({'post':'getAccountProfile'}),name='account-profile'),
]