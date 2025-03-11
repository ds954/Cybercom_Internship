from .models import UserInfo

def user_profile(request):
    user_data = None
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user_data = UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            user_data = None

    return {'profile_user': user_data}
