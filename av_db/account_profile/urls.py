from tkinter.font import names

from django.urls import path, include
from rest_framework.routers import DefaultRouter


from account_profile.controller.account_profile_controller import AccountProfileController

router = DefaultRouter()
router.register(r'account-profile', AccountProfileController, basename='account-profile')

urlpatterns = [
    path('', include(router.urls)),
]