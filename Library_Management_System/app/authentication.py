import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from .models import UserInfo, RefreshTokenStore
from datetime import datetime
from django.shortcuts import redirect

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request) #This extracts the token from the HTTP request header.
        
        if not auth_data:
            return None #If the Authorization header is missing, it returns None, meaning the user is not authenticated.


        prefix, token = auth_data.decode('utf-8').split(' ')

        if prefix != 'Bearer':
            return None #If the prefix is not "Bearer", it means the token is not valid.


        try:
            payload = jwt.decode(token, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']]) #payload['email']: Extracts the user's email from the token.
            user = UserInfo.objects.get(email=payload['email']) #Finds the user in the database

            # Check refresh token validity on every request
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                raise exceptions.AuthenticationFailed('Refresh token missing')
            try:
                jwt.decode(refresh_token, settings.JWT_AUTH['JWT_SECRET_KEY'], algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']])
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Refresh token expired')

            return (user, token)

        except jwt.ExpiredSignatureError:
            return self.refresh_access_token(request)

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except UserInfo.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid user')

        return None

    def refresh_access_token(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None

        try:
            prefix, token = auth_data.decode('utf-8').split(' ')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token format')

        if prefix != 'Bearer':
            return None

        try:
            payload = jwt.decode(
                token, 
                settings.JWT_AUTH['JWT_SECRET_KEY'], 
                algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']],
                options={"verify_signature": False}  # Allow decoding expired token
            )
            user = UserInfo.objects.get(email=payload['email'])
            refresh_token_obj = RefreshTokenStore.objects.filter(user=user).first()
            
            if not refresh_token_obj:
                raise exceptions.AuthenticationFailed("Refresh token missing")

            refresh_token = refresh_token_obj.token

            try:
                refresh_payload = jwt.decode(
                    refresh_token, 
                    settings.JWT_AUTH['JWT_SECRET_KEY'], 
                    algorithms=[settings.JWT_AUTH['JWT_ALGORITHM']]
                )

                access_token_payload = {
                    'email': user.email,
                    'exp': datetime.now() + settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'],
                    'iat': datetime.now(),
                }
                access_token = jwt.encode(
                    access_token_payload, 
                    settings.JWT_AUTH['JWT_SECRET_KEY'], 
                    algorithm=settings.JWT_AUTH['JWT_ALGORITHM']
                )

                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
                return (user, access_token)

            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Session expired. Please login again.')
            except jwt.DecodeError:
                raise exceptions.AuthenticationFailed('Invalid refresh token')

        except (UserInfo.DoesNotExist, RefreshTokenStore.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid user or refresh token')

        return None
