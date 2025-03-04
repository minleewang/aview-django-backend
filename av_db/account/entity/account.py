from django.db import models

from account.entity.account_role_type import AccountRoleType
from account_profile.entity.account_profile import AccountProfile


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    roleType = models.ForeignKey(AccountRoleType, on_delete=models.CASCADE) # 디폴트값 = NORMAL

    accountProfile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)  #, related_name ="profile")


    def __str__(self):
        return f"Account -> id: {self.id}, roleType: {self.roleType}"

    class Meta:
        db_table = 'account'
        app_label = 'account'

