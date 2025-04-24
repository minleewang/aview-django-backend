from django.apps import AppConfig

class InterviewTechStackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interview_tech_stack'  # ✅ 이 이름이 INSTALLED_APPS와 정확히 일치해야 함!
