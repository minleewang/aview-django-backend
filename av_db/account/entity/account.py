from django.db import models

from account.entity.account_role_type import AccountRoleType


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32)
    gender = models.CharField(max_length=32, default="Unknown") # 성별 추가
    birthyear = models.IntegerField(default="Unknown") # 생년월일 추가
    loginType = models.CharField(max_length=32, default="KAKAO")
    roleType = models.ForeignKey(AccountRoleType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'account'
        app_label = 'account'

    def getId(self):
        return self.id

    def getEmail(self):
        return self.email
