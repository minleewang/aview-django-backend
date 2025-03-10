from django.db import models

from account.entity.account_role_type import AccountRoleType
from account.entity.account_login_type import AccountLoginType


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=32)
    gender = models.CharField(max_length=32, default="Unknown") # 성별 추가
    birthyear = models.IntegerField(default="Unknown") # 생년월일 추가
    age_range = models.CharField(max_length=32)
    roleType = models.ForeignKey(AccountRoleType, on_delete=models.CASCADE)
    loginType = models.ForeignKey(AccountLoginType, on_delete=models.CASCADE)  # , related_name ="profile")

    def __str__(self):
        return f"Account(id={self.id}, email={self.email}, gender={self.gender}, age_range={self.age_range}, loginType={self.loginType})"

    class Meta:
        db_table = 'account'
        app_label = 'account'

    def getId(self):
        return self.id

    def getEmail(self):
        return self.email
