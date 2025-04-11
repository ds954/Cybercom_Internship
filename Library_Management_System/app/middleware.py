from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import redirect
from django.urls import resolve

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        new_access_token = getattr(request, 'new_access_token', None)

        if new_access_token:
            response.set_cookie(
                'access_token',
                new_access_token,
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=settings.JWT_AUTH['JWT_ACCESS_TOKEN_LIFETIME'].total_seconds()
            )
        return response
    
# class AuthenticationRedirectMiddleware(MiddlewareMixin):
#     def process_exception(self, request, exception):

       
#         if isinstance(exception, AuthenticationFailed):
#             if not request.path.startswith('/admin/'):
#                 print("AuthenticationFailed caught in middleware. Redirecting to login...")
#                 print("AuthenticationFailed caught in middleware. Redirecting to login...")
#                 response = redirect('login')
#                 response.delete_cookie('access_token')  # Remove expired tokens
#                 response.delete_cookie('refresh_token')
#                 return response  # Redirect user to login
#         return None  # Continue normal flow if not AuthenticationFailed


class AuthenticationRedirectMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        print(f"Request path: {request.path}")
        print(f"Exception: {exception}")
        try:
            resolved_path = resolve(request.path)
            if resolved_path.app_name == 'admin':
                print("Skipping authentication for Django Admin.")
                return None
        except:
            pass
        excluded_paths = [
            '/admin/',
            '/login/',
            '/logout/',
            '/register/',
            '/reset_password/',
            '/otp/',
            '/email/'
        ]

        # Check if the path is excluded
        if any(request.path.startswith(path) for path in excluded_paths):
            print(f"Path {request.path} is excluded. Not redirecting on AuthenticationFailed.")
            return None

        print("Path not excluded. Proceeding with potential redirect for JWT auth failure.")
        if isinstance(exception, AuthenticationFailed):
            print("AuthenticationFailed caught in middleware. Redirecting to login...")
            response = redirect('login')
            response.delete_cookie('access_token')  # Remove expired tokens
            response.delete_cookie('refresh_token')
            return response  # Redirect user to login
        return None  # Continue normal flow if not AuthenticationFailed