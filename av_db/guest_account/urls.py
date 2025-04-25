from django.urls import path, include
from rest_framework.routers import DefaultRouter

from guest_account.controller.guest_account_controller import GuestAccountController

router = DefaultRouter()
router.register(r"guest_account", GuestAccountController, basename='guest_account')

urlpatterns = [
    path('', include(router.urls)),
    path('request-email',
         GuestAccountController.as_view({ 'post': 'requestEmail' }),
         name='이메일 요청'),
]