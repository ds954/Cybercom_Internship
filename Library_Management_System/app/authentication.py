from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from datetime import datetime, timedelta
import jwt
import time
from .models import UserInfo, RefreshTokenStore

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        print(f"\nAuthenticating {request.path}...")

        if request.path in ['/login/', '/logout/']:
            print("Skipping auth for login/logout")
            return None

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")

        if access_token:
            try:
                payload = jwt.decode(
                    access_token,
                    settings.JWT_AUTH['JWT_SECRET_KEY'],
                    algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']]
                )
                print("Access token valid.")
                user = UserInfo.objects.get(email=payload['email'])
                # request.user = user
                return (user, None)

            except jwt.ExpiredSignatureError:
                print("Access token expired. Trying refresh...")
            except jwt.DecodeError:
                print("Access token invalid.")
                raise AuthenticationFailed('Invalid access token.')

        if not refresh_token:
            print("No refresh token found. Raising AuthenticationFailed.")
            raise AuthenticationFailed('Authentication credentials were not provided. Please login.')

        # Refresh token handling
        try:
            refresh_payload = jwt.decode(
                refresh_token,
                settings.JWT_AUTH['JWT_SECRET_KEY'],
                algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']]
            )
            user = UserInfo.objects.get(email=refresh_payload['email'])

            refresh_token_obj = RefreshTokenStore.objects.filter(
                user=user,
                token=refresh_token
            ).first()

            if not refresh_token_obj:
                print("Refresh token not found in DB. Raising AuthenticationFailed.")
                raise AuthenticationFailed('Invalid refresh token.')

            # Generate a new access token
            new_access_token_payload = {
                'email': user.email,
                'exp': datetime.utcnow() + settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'],
                'iat': int(time.time()),
            }

            new_access_token = jwt.encode(
                new_access_token_payload,
                settings.JWT_AUTH['JWT_SECRET_KEY'],
                algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
            )

            request.new_access_token = new_access_token
            print("New access token generated and set on request.")
            return (user, None)

        except jwt.ExpiredSignatureError:
            print("Refresh token expired. Raising AuthenticationFailed.")
            raise AuthenticationFailed('Refresh token expired. Please login again.')

        except jwt.DecodeError:
            print("Invalid refresh token. Raising AuthenticationFailed.")
            raise AuthenticationFailed('Invalid refresh token.')
