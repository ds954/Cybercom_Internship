from .models import Notification
from .models import UserInfo
from django.shortcuts import get_object_or_404
def user_profile(request):
    user_data = None
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user_data = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            user_data = None

    return {'profile_user': user_data}


def notification_count(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(UserInfo, id=user_id)

   
    count = Notification.objects.filter(user=user, is_read=False).count()
    return {'notification_count': count}