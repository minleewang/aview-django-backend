from django.db.models import IntegerChoices


class AcademicBackground(IntegerChoices):
    MAJOR = 1, "전공자"
    NON_MAJOR = 2, "비전공자"