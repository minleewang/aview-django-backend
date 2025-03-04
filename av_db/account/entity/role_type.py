from django.db import models

class RoleType(models.TextChoices):
    ADMIN = 'ADMIN'
    NORMAL = 'NORMAL'
    #BLACKLIST = 'BLACKLIST'

    # 디폴트는 Normal
    # ADMIN은 팀 5명이니 수동으로 지정해서 DB에 저장하기