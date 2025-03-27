from .models import Notification
from .models import UserInfo
from django.shortcuts import get_object_or_404
from .authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

# def user_profile(request):
#     user_data = JWTAuthentication().authenticate(request)  # Authenticate user manually
#     print("Context Processor User Data:", user_data)  # Debugging print

#     if not user_data:
#         return {}  # No user detected

#     user, _ = user_data
#     return {'profile_user': user}  # Pass user to templates

from .models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
from .authentication import JWTAuthentication  # Import your JWT auth class
def user_context_processor(request):  #  Ensure this matches the settings.py entry
    """ Context processor to provide authenticated user to all templates """
    print(" Context processor executed")  # Debugging line

    try:
        print(" Context processor executed for", request.path)
        user_data = JWTAuthentication().authenticate(request)
        if not user_data:
            print(" No user authenticated")
            return {}  # No user authenticated

        user, _ = user_data
        print(f" Authenticated user: {user}")  # Debugging line
        return {'profile_user': user}  #  Ensure this key is correct

    except ObjectDoesNotExist:
        print(" User not found")
        return {'profile_user': None}  

    except Exception as e:
        print(f" Context Processor Error: {e}")
        return {'profile_user': None}  



def notification_count(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

   
    count = Notification.objects.filter(user=user, is_read=False).count()
    return {'notification_count': count}