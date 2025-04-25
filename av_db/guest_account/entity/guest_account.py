from django.db import models


class GuestAccount(models.Model):
    id = models.AutoField(primary_key=True)  # 내부용 숫자 ID
    email = models.CharField(max_length=32)
    loginType = models.CharField(max_length=16, default='guest', editable=False)  # guest 고정

    def __str__(self):
        return f"GuestAccount(id={self.id}, email={self.email}, loginType={self.loginType})"

    class Meta:
        db_table = 'guest_account'
        app_label = 'guest_account'

    def getId(self):
        return self.id

    def getEmail(self):
        return self.email

    def getLoginType(self):
        return self.loginType
