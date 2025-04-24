from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from django.utils.timezone import now
import time
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import Group
import time
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle
from datetime import datetime,timedelta

import time
from datetime import timedelta, datetime
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
import time

class PaidUserRateThrottle(BaseThrottle):
    """
    A custom throttle that limits request rates based on whether a user
    belongs to the 'PaidUser' group. Paid users have a higher request limit.
    Uses Django's cache to track request history.
    """
    # Format string for the cache key. It includes the throttling scope
    # ('paid' or 'free') and the user's unique identifier.
    cache_format = 'throttle_%(scope)s_%(ident)s'

    def __init__(self):
        """
        Initializes instance variables to store rate, duration, scope,
        number of allowed requests, and the user identifier.
        """
        self.rate = None        # Not directly used here, calculated dynamically
        self.duration = None    # The time window for throttling (e.g., 1 day)
        self.scope = None       # 'paid' or 'free' based on user group
        self.num_requests = None # Number of requests allowed within the duration
        self.ident = None       # User identifier (primary key) for tracking

    def allow_request(self, request, view):
        """
        Determines if the current request should be allowed based on the
        user's request history and their throttling tier.
        """
        # Allow requests from anonymous (non-logged-in) users without throttling.
        if not request.user or not request.user.is_authenticated:
            return True

        # Get the authenticated user object.
        user = request.user
        # Get the user's primary key as a string to use as a unique identifier.
        ident = str(user.pk)
        # Store the user identifier for use in the wait() method.
        self.ident = ident

        # Determine the throttling scope and limits based on the user's group.
        if user.groups.filter(name='PaidUser').exists():
            self.scope = 'paid'
            self.num_requests = 4
            self.duration = 60 * 60 * 24  # 1 day in seconds
        else:
            self.scope = 'free'
            self.num_requests = 2
            self.duration = 60 * 60 * 24

        # Construct the cache key using the scope and user identifier.
        cache_key = self.cache_format % {'scope': self.scope, 'ident': ident}
        # Retrieve the request history (list of timestamps) from the cache.
        # If no history exists, default to an empty list.
        history = cache.get(cache_key, [])
        # Get the current timestamp.
        now = time.time()

        # Filter out timestamps of requests that occurred outside the throttling window.
        history = [t for t in history if now - t < self.duration]

        # If the number of recent requests is greater than or equal to the allowed limit,
        # the request should be throttled (not allowed).
        if len(history) >= self.num_requests:
            return False  # Throttle

        # If the request is allowed, add the current timestamp to the history.
        history.append(now)
        # Store the updated history back in the cache with a timeout equal to the throttling duration.
        cache.set(cache_key, history, timeout=self.duration)
        # Indicate that the request should be allowed.
        return True

    def wait(self):
        """
        Calculates the number of seconds to wait before the next request is allowed
        when a request has been throttled.
        """
        # If the user identifier or scope hasn't been determined, we can't calculate
        # the wait time, so return None.
        if not self.ident or not self.scope:
            return None

        # Construct the cache key again to retrieve the request history.
        cache_key = self.cache_format % {'scope': self.scope, 'ident': self.ident}
        history = cache.get(cache_key, [])
        now = time.time()
        # Filter out old requests to consider only those within the current window.
        history = [t for t in history if now - t < self.duration]

        # If there's a history of recent requests (meaning the throttle was hit):
        if history:
            # Find the timestamp of the earliest (oldest) request in the recent history.
            earliest = min(history)
            # Calculate the remaining time until that earliest request falls outside the
            # throttling window. This is the time the user needs to wait.
            remaining_time = self.duration - (now - earliest)
            # Return the remaining time, rounded to one decimal place, ensuring it's not negative.
            return max(0, round(remaining_time, 1))
        # If there's no recent history (which shouldn't happen if throttled, but as a fallback),
        # return 0, indicating no wait time.
        return 0

# import time
# from django.core.cache import cache
# from rest_framework.throttling import BaseThrottle

# class PaidUserRateThrottle(BaseThrottle):
#     cache_format = 'throttle_%(scope)s_%(ident)s'

#     def allow_request(self, request, view):
#         # Anonymous user
#         if not request.user or not request.user.is_authenticated:
#             ident = 'anon_' + request.META.get('REMOTE_ADDR', '')
#             print(f"[Throttle] Anonymous user. Applying free limit to ident: {ident}")
#             return self._check_limit('free', ident, 2)

#         user = request.user
#         user_groups = list(user.groups.values_list('name', flat=True))
#         print(f"[Throttle] Authenticated user: {user.username}, Groups: {user_groups}")

#         # Paid users
#         print("True?",user.groups.filter(name__in=['MonthlySubscriber', 'YearlySubscriber']).exists())
#         if user.groups.filter(name__in=['MonthlySubscriber', 'YearlySubscriber']).exists():
#             cache_key = f'subscription_start_{user.pk}'
#             subscription_start = cache.get(cache_key)
#             print("start the subscription",subscription_start)
#             if not subscription_start:
#                 subscription_start = datetime.now() - timedelta(days=10)
#                 cache.set(cache_key, subscription_start, timeout=None)
#                 print(f"[Throttle] Setting fake subscription start date to {subscription_start}")
           
#                 # Calculate expiry date (30 days after subscription start)
#                 expiry_date = subscription_start + timedelta(days=30)
#                 print(f"[Throttle] Subscription start date: {subscription_start}, Expiry date: {expiry_date}")
                
#                 # If subscription is still valid (within 30 days), allow unlimited access
#                 if datetime.now() < expiry_date:
#                     print(f"[Throttle] User {user.username} has a valid subscription. Unlimited access granted.")
#                     return True
#                 else:
#                     print(f"[Throttle] User {user.username}'s subscription expired after 30 days.")
#                     return False  # Throttle expired user
#             else:
#                 print(f"[Throttle] Subscription data missing for user {user.username}. Throttling access.")
#                 return False  # Throttle user if subscription data is missing

#         # Free users
#         print(f"[Throttle] User {user.username} is not a subscriber. Applying rate limit.")
#         return self._check_limit('free', str(user.pk), 2)

#     def _check_limit(self, scope, ident, rate_limit,subscription_start=None):
#         cache_key = self.cache_format % {'scope': scope, 'ident': ident}
#         now = time.time()
#         duration = 60 * 60 * 24  # 1 day

#         if subscription_start:
#             # Calculate the subscription expiry date (30 days after subscription start)
#             expiry_date = subscription_start + timedelta(days=30)
#             print(f"[Throttle] Subscription start date: {subscription_start}, Expiry date: {expiry_date}")
            
#             # If current time is past expiry date, return throttled access
#             if datetime.now() > expiry_date:
#                 print(f"[Throttle] Subscription expired for {ident}!")
#                 return False  # Throttle user (access denied)

#         # Clean up old requests
#         history = cache.get(cache_key, [])
#         history = [t for t in history if now - t < duration]
#         print(f"[Throttle] Request history for {ident} (limit {rate_limit}/day): {len(history)} requests in last 24h")

#         if len(history) >= rate_limit:
#             print(f"[Throttle] Throttle limit exceeded for {ident}")
#             return False

#         history.append(now)
#         cache.set(cache_key, history, timeout=duration)
#         print(f"[Throttle] Access granted for {ident}, remaining: {rate_limit - len(history)}")
#         return True
import math

class FreeUserRateThrottle(UserRateThrottle):
    scope = 'free'
    rate = '2/day'

    def wait(self):
        return super().wait()  # or return self.duration if you override throttling logic


# class PaidUserRateThrottle(UserRateThrottle):
#     scope = 'paid'
#     rate = '4/day'

class RoleBasedThrottle(BaseThrottle):
    """
    A custom throttle that limits request rates based on the user's role
    (specifically, whether they are a staff member). Staff members are
    allowed a higher request rate. Uses Django's cache to track requests.
    """
    def allow_request(self, request, view):
        """
        Determines if the current request should be allowed based on the
        user's authentication status and staff status.
        """
        # Allow requests from unauthenticated users without throttling.
        if not request.user.is_authenticated:
            return True

        # Get the primary key (ID) of the authenticated user.
        ident = request.user.pk
        # Check if the authenticated user is a staff member.
        is_staff = request.user.is_staff
        print(is_staff)  # For debugging purposes, prints whether the user is staff.

        # Define the allowed request rate based on staff status.
        # Staff members get 5 requests, others get 3 requests within the duration.
        rate = 5 if is_staff else 3
        # Define the throttling duration in seconds (1 minute in this case).
        duration = 60

        # Construct a unique cache key based on the user's staff status and ID.
        # This ensures separate tracking for staff and non-staff users.
        cache_key = f"throttle_{'staff' if is_staff else 'normal'}_{ident}"
        print(cache_key)  # For debugging purposes, prints the generated cache key.

        # Retrieve the request history (list of timestamps) from the cache.
        # If no history exists, default to an empty list.
        history = cache.get(cache_key, [])

        # Get the current timestamp.
        now_ts = time.time()
        # Filter out timestamps of requests that occurred outside the throttling window (last 'duration' seconds).
        history = [t for t in history if t > now_ts - duration]

        # If the number of recent requests is greater than or equal to the allowed rate,
        # the request should be throttled (not allowed).
        if len(history) >= rate:
            return False

        # If the request is allowed, add the current timestamp to the history.
        history.append(now_ts)
        # Store the updated history back in the cache with a timeout equal to the throttling duration.
        cache.set(cache_key, history, duration)
        # Indicate that the request should be allowed.
        return True