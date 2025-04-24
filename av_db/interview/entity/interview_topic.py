from django.db.models import IntegerChoices

class InterviewTopic(IntegerChoices):
    BACKEND = 1, "Backend"
    FRONTEND = 2, "Frontend"
    EMBEDDED = 3, "Embedded"
    AI = 4, "AI"
    DEVOPS = 5, "DevOps"
    WEBAPP = 6, "App·Web"