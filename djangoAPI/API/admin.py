from django.contrib import admin
from oauth2_provider.models import get_application_model
from oauth2_provider.admin import ApplicationAdmin as DefaultApplicationAdmin
from .models import UserInfo

admin.site.register(UserInfo)
Application = get_application_model()

# Unregister the default one if it's already registered
if admin.site.is_registered(Application):
    admin.site.unregister(Application)

# Define your custom admin class
class CustomApplicationAdmin(DefaultApplicationAdmin):
    readonly_fields = ('client_id', 'client_secret')

# Register it again with your custom admin class
admin.site.register(Application, CustomApplicationAdmin)
