from django.urls import path, include
from rest_framework.routers import DefaultRouter

from google_oauth.controller.google_oauth_controller import GoogleOauthController

router = DefaultRouter()
router.register(r"guest-oauth", GoogleOauthController, basename='guest-oauth')

urlpatterns = [
    path('', include(router.urls)),
    path('request-login-url',
         GoogleOauthController.as_view({ 'post': 'requestGuestSignIn' }),
         name='Google Oauth 링크 요청'),
    path('request-user-token',
         GoogleOauthController.as_view({ 'post': 'requestUserToken' }),
         name='User Token 요청'),

]