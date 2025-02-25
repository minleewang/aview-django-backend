from django.db import models

class LoginType(models.TextChoices):
    KAKAO = 'KAKAO', 'Kakao'
    GENERAL = 'NORMAL', 'normal'
    GOOGLE = 'GOOGLE', 'google'
    NAVER = 'NAVER' ,'naver'