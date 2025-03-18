from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import redirect

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        new_access_token = getattr(request, 'new_access_token', None)

        if new_access_token:
            response.set_cookie(
                'access_token',
                new_access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds()
            )
        return response
    
class AuthenticationRedirectMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, AuthenticationFailed):
            print("AuthenticationFailed caught in middleware. Redirecting to login...")
            response = redirect('login')
            response.delete_cookie('access_token')  # Remove expired tokens
            response.delete_cookie('refresh_token')
            return response  # Redirect user to login
        return None  # Continue normal flow if not AuthenticationFailed
  