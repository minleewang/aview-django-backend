from django.db import models
from account.entity.account import Account


from account_profile.entity.account_profile_gender_type import AccountProfileGenderType


class AccountProfile(models.Model):
    nickname = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32, default=None, null=True)  # 일반 회원가입일 경우 사용하는 비밀번호
    salt = models.CharField(max_length=16, default=None, null=True)
    gender = models.ForeignKey(AccountProfileGenderType, on_delete=models.CASCADE)   # 성별 필드 추가
    birthyear = models.IntegerField()           # 생년월일 필드 추가
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    def __str__(self):
        return f"Profile -> email: {self.email}, nickname: {self.nickname}"

    class Meta:
        db_table = 'account_profile'
        app_label = 'account_profile'
