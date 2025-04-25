from django.db.models import IntegerChoices


class ProjectExperience(IntegerChoices):
    NO_PROJECT = 0, "없음"
    HAS_PROJECT = 1, "있음"
