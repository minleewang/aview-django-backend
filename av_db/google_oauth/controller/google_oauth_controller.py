import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from account.service.account_service_impl import AccountServiceImpl
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from google_oauth.serializers.google_oauth_access_token_serializer import GoogleOauthAccessTokenSerializer
from google_oauth.service.google_oauth_service_impl import GoogleOauthServiceImpl
from redis_service.service.redis_service_impl import RedisServiceImpl


class GoogleOauthController(viewsets.ViewSet):
    googleOauthService = GoogleOauthServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    accountProfileService = AccountProfileServiceImpl.getInstance()

    def get_account(self):
        from account_profile.entity.account_profile import AccountProfile
        return AccountProfile

    def requestGoogleOauthLink(self, request):
        url = self.googleOauthService.requestGoogleOauthLink()

        return JsonResponse({"url": url}, status=status.HTTP_200_OK)

    def requestGoogleAccessToken(self, request):
        serializer = GoogleOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        print(f"code: {code}")

        try:
            tokenResponse = self.googleOauthService.requestGoogleAccessToken(code)
            accessToken = tokenResponse['access_token']
            print(f"accessToken: {accessToken}")

            with transaction.atomic():
                userInfo = self.googleOauthService.requestUserInfo(accessToken)
                user_id = userInfo.get('id', '') # 사용자 ID
                nickname = userInfo.get('properties', {}).get('nickname', '') # 닉네임
                email = userInfo.get('google_account', {}).get('email', '') # 이메일
                gender = userInfo.get('google_account', {}).get('gender', '')  # 성별별
                age_range = userInfo.get('google_account', {}).get('age_range', '') # 연령대
                birthyear = userInfo.get('google_account', {}).get('birthyear', '') # 출생연도
                # 정보 출력 (디버깅용)
                # print(f"email: {email}, nickname: {nickname}")
                print(f"user_id: {user_id}, email: {email}, nickname: {nickname}")
                print(f"gender: {gender}, age_range: {age_range}, birthyear: {birthyear}")

                # 이메일 형식 확인
                accountProfile = self.accountProfileService.checkEmailDuplication(email)
                print(f"accountProfile: {accountProfile}")

                if accountProfile is None:
                    accountProfile = self.accountProfileService.createAccountProfile(email)
                    print(f"accountProfile: {accountProfile}")

                    accountProfile = self.accountProfileService.createAccountProfile(
                        accountProfile.getId()
                    )
                    print(f"accountProfile: {accountProfile}")

                # account = self.accountService.checkEmailDuplication(email)
                # print(f"account: {account}")

                userToken = self.__createUserTokenWithAccessToken(accountProfile, accessToken)
                print(f"userToken: {userToken}")
            
            return JsonResponse({'userToken: userToken'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        #     if account is None:
        #         account = self.accountService.createAccount(email)
        #         print(f"account: {account}")

        #         accountProfile = self.accountProfileService.createAccountProfile(
        #             account.getId(), nickname
        #         )
        #         print(f"accountProfile: {accountProfile}")

        #     userToken = self.__createUserTokenWithAccessToken(account, accessToken)
        #     print(f"userToken: {userToken}")

        #     return JsonResponse({'userToken': userToken})

        # except Exception as e:
        #     return JsonResponse({'error': str(e)}, status=500)


    def requestUserToken(self, request):
        access_token = request.data.get('access_token')  # 클라이언트에서 받은 access_token
        user_id = request.data.get('id')    # 클라이언트에서 받은 id
        email = request.data.get('email')  # 클라이언트에서 받은 email
        nickname = request.data.get('nickname')  # 클라이언트에서 받은 nickname
        gender = request.data.get('gender') # 클라이언트에서 받은 성별
        age_range = request.data.get('age_range')   # 클라이언트에서 받은 연령대
        birthyear = request.data.get('birthyear')   # 클라이언트에서 받은 출생연도

        print(f'is operate?')

        if not access_token:
            return JsonResponse({'error': 'Access token is required'}, status=400)

        if not email or not nickname or not gender or not age_range or not birthyear:
            return JsonResponse({'error': 'All user information (ID, email, nickname, gender, age_range, birthyear) is required'}, status=400)

        try:
            # 이메일을 기반으로 계정을 찾거나 새로 생성합니다.
            accountProfile = self.accountProfileService.checkEmailDuplication(email)
            if accountProfile is None:
                account = self.accountService.createAccount(email)
                accountProfile = self.accountProfileService.createAccountProfile(
                    account.getId(), nickname
                )

            # 사용자 토큰 생성 및 Redis에 저장
            userToken = self.__createUserTokenWithAccessToken(account, access_token)

            return JsonResponse({'userToken': userToken})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def __createUserTokenWithAccessToken(self, accountProfile, accessToken):
        try:
            userToken = str(uuid.uuid4())
            self.redisService.storeKeyValue(accountProfile.getId(), accessToken)
            self.redisService.storeKeyValue(userToken, accountProfile.getId())

            return userToken

        except Exception as e:
            print('Redis에 토큰 저장 중 에러:', e)
            raise RuntimeError('Redis에 토큰 저장 중 에러')

    def dropRedisTokenForLogout(self, request):
        try:
            userToken = request.data.get('userToken')
            isSuccess = self.RedisService.deleteKey(userToken)

            return Response({'isSuccess': isSuccess}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f'레디스 토큰 해제 중 에러 발생:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
