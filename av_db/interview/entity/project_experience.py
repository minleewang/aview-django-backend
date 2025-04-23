from django.db.models import IntegerChoices


class ProjectExperience(IntegerChoices):
    HAS_PROJECT = 1, "있음"
    NO_PROJECT = 2, "없음"