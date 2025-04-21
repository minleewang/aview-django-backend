from django.db import models

'''''
class InterviewTopic(models.TextChoices):
    BACKEND = 1, "Backend", "백엔드"
    FRONTEND = 2,  "Frontend", "프론트엔드"
    EMBEDDED =3, "Embedded", "임베디드"
    AI =4, "AI", "인공지능"
    DEVOPS =5, "DevOps", "데브옵스"
    WEBAPP =6, "AppWeb", "앱웹"
'''

from django.db.models import IntegerChoices

class InterviewTopic(IntegerChoices):
    BACKEND = 1, "Backend"
    FRONTEND = 2, "Frontend"
    EMBEDDED = 3, "Embedded"
    AI = 4, "AI"
    DEVOPS = 5, "DevOps"
    WEBAPP = 6, "App·Web"
