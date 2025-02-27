import requests

from av_db import settings
from naver_oauth.repository.naver_oauth_repository import NaverOauthRepository


class NaverOauthRepositoryImpl(NaverOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.loginUrl = settings.NAVER['LOGIN_URL']
            cls.__instance.clientId = settings.NAVER['CLIENT_ID']
            cls.__instance.clientSecret = settings.NAVER['CLIENT_SECRET']
            cls.__instance.redirectUri = settings.NAVER['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.NAVER['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.NAVER['USERINFO_REQUEST_URI']
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        print("getOauthLink() for Login")

        return (f"{self.loginUrl}/oauth/authorize?"
                f"client_id={self.clientId}&redirect_uri={self.redirectUri}&response_type=code")

    def getAccessToken(self, code):
        accessTokenRequest = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'redirect_uri': self.redirectUri,
            'code': code,
            'client_secret': None
        }

        response = requests.post(self.tokenRequestUri, data=accessTokenRequest)
        return response.json()

    def getUserInfo(self, accessToken):
        headers = {'Authorization': f'Bearer {accessToken}'}
        response = requests.post(self.userInfoRequestUri, headers=headers)
        return response.json()
