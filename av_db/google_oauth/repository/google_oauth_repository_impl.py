import requests

from av_db import settings
from google_oauth.repository.google_oauth_repository import GoogleOauthRepository


class GoogleOauthRepository(GoogleOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.loginUrl = settings.GOOGLE['LOGIN_URL']
            cls.__instance.clientId = settings.GOOGLE['CLIENT_ID']
            cls.__instance.redirectUri = settings.GOOGLE['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.GOOGLE['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.GOOGLE['USER_INFO_REQUEST_URI']

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
