
# from rest_framework.throttling import UserRateThrottle
# from rest_framework.exceptions import Throttled
# import math

# class CustomUserRateThrottle(UserRateThrottle):
#     def get_cache_key(self, request, view):
#         print("get cashe key method called:")
#         if not request.user or not request.user.is_authenticated:
#             return None
#         self.user = request.user
#         return self.cache_format % {
#             'scope': self.scope,
#             'ident': request.user.pk
#         }

#     def get_rate(self):
#         print("get_rate method called")
#         if not hasattr(self, 'user') or not self.user.is_authenticated:
#             return super().get_rate()

#         # Set different limits for multiple users (example: username based)
#         user_limits = {
#             'admin': '3/day',
#             'dhara': '1/day',
         
#         }

#         # Check if the user is in the dictionary, otherwise return default
#         rate = user_limits.get(self.user.username, '5/day')  # Default rate if user is not found
#         return rate

#     def throttle_failure(self):
#         wait = self.wait()
#         wait_hours = math.ceil(wait / 3600) if wait else 0
#         detail = f"Request was throttled. Try again in {wait_hours} hour(s)."
#         raise Throttled(detail=detail, wait=wait)
from rest_framework.throttling import UserRateThrottle

class PaidUserRateThrottle(UserRateThrottle):
    scope = 'paid'
    rate = '4/day'

class FreeUserRateThrottle(UserRateThrottle):
    scope = 'free'
    rate = '2/day'

class UserSpecificRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            print("yes authenticated")
            if request.user.is_staff:
                self.rate = '4/min' # Example for staff users
            else:
                self.rate = '2/min' # Example for regular users
            return self.cache_format % {
                'scope': self.scope,
                'ident': self.get_ident(request, view)
            }
        else:
             return None # Anonymous users are not throttled by this class

class DynamicUserRateThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        print("get_cache_key")
        if request.user and request.user.is_authenticated:
            print("user",request.user)
            print("user is authenticated?",request.user.is_authenticated)
            print("user is admin?",request.user.is_staff)
            self.user = request.user
            if request.user.is_staff:
                self.rate = "4/min"
            else:
                self.rate = "2/min"
            print(f"Rate set in get_cache_key for {request.user.username}: {self.rate}")
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }
        return None
    
    
    def get_rate(self):
        # Fetch user directly from the request object passed into allow_request
        user = getattr(self, 'user', None)
        print("this is user: ",user)

        print("calling get_rate:")
        if user and user.is_authenticated:
            if user.is_staff:
                rate = "4/min"
            else:
                rate = "2/min"
            print(f"Rate set in get_rate for {user.username}: {rate}")
            return rate

        print("Default anonymous rate: 1/min")
        return "1/min"
# class DynamicUserRateThrottle(UserRateThrottle):
#     scope = 'user'  # This matches your view's throttle_scope
    
#     def get_rate(self):
#         if self.request.user.is_authenticated:
#             if self.request.user.is_staff:
#                 return '4/min'
#             return '2/min'
#         return '1/min'
    
#     def get_cache_key(self, request, view):
#         if request.user.is_authenticated:
#             return self.cache_format % {
#                 'scope': self.scope,
#                 'ident': request.user.pk
#             }
#         return None
    
#     def allow_request(self, request, view):
#         self.request = request
        
#         # Determine the actual rate based on user status
#         if request.user.is_authenticated:
#             if request.user.is_staff:
#                 self.rate = '4/min'
#             else:
#                 self.rate = '2/min'
#         else:
#             self.rate = '1/min'
#         print(f"Final rate being used: {self.get_rate()}")
#         return super().allow_request(request, view)