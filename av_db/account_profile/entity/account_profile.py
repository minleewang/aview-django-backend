from django.db import models
from account.entity.account import Account
from account_profile.entity.account_login_type import AccountLoginType


class AccountProfile(models.Model):
    id = models.AutoField(primary_key=True)
    profile_nickname = models.CharField(max_length=32, unique=True)
    account_email = models.CharField(max_length=32, unique=True)
    gender = models.CharField(max_length=32, unique=True)
    age_range = models.IntegerField()
    birthyear = models.IntegerField()
    loginType = models.ForignKey(AccountLoginType, on_delete=models.CASCADE) #, related_name ="profile")

    #account = models.OneToOneField(
    #    Account,
    #    on_delete=models.CASCADE,
    #    related_name ="profile"
    #)
    # account를 참조하지 않은 이유 : 우선 account_profile은 카카오 로그인을 통해 받은 정보를 account_profile DB에 저장만 하기 때문
    # account_profile에서 따로 회원들의 프로필을 생성하지 않음. 전체 데이터일뿐


    def __str__(self):
        return f"Profile -> email: {self.email}, nickname: {self.nickname}"

    class Meta:
        db_table = 'account_profile'
        app_label = 'account_profile'

