from django.contrib import admin
from .models import UserInfo
from django.contrib import admin
from oauth2_provider.models import Application
# from rest_framework.authtoken.models import Token 
# Register your models here.
admin.site.register(UserInfo)

admin.site.unregister(Application)

class OAuthClientAdmin(admin.ModelAdmin):
    readonly_fields = ('client_id', 'client_secret')  # make them read-only

admin.site.register(Application, OAuthClientAdmin)



# class Tokendisplay(admin.ModelAdmin):
#     list_display=['key','user', 'created']
# admin.site.register(Token, Tokendisplay)
