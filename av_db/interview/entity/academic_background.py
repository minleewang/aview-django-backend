from django.db.models import IntegerChoices


class AcademicBackground(IntegerChoices):
    NON_MAJOR = 0, "비전공자"
    MAJOR = 1, "전공자"
