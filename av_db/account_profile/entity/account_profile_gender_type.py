from django.db import models

from account_profile.entity.gender_type import GenderType

class AccountProfileGenderType(models.Model):
    gender_type = models.CharField(max_length=10, choices=GenderType.choices, unique=True)

    def __str__(self):
        return self.gender_type
    
    class Meta:
        db_table = 'account_profile_gender_type'
        app_label = 'account_profile'