# interview/entity/interview_company.py

from django.db.models import TextChoices

class InterviewCompany(TextChoices):
    DANGGEUN = "danggeun", "당근마켓"
    TOSS = "toss", "Toss"
    SK_ENCORE = "sk_encore", "SK엔코아"
    KT_MOBILE = "kt_mobile", "KT모바일"
