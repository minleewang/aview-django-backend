from django.db import models

class GenderType(models.TextChoices):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
