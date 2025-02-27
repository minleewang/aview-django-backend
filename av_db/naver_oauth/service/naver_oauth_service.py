from abc import ABC, abstractmethod


class NaverOauthService(ABC):

    @abstractmethod
    def requestNaverOauthLink(self):
        pass

    @abstractmethod
    def requestNaverAccessToken(self, code):
        pass

    @abstractmethod
    def requestUserInfo(self, accessToken):
        pass
