from django.db.models import IntegerChoices

class InterviewTopic(IntegerChoices):
    BACKEND = 1, "Backend"
    FRONTEND = 2, "Frontend"
    EMBEDDED = 3, "App·Web"
    AI = 4, "AI"
    DEVOPS = 5, "Embedded"
    WEBAPP = 6, "DevOps"