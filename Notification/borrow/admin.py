from django.contrib import admin
from .models import BorrowRequest# Replace .models with your apps model location.

admin.site.register(BorrowRequest)
# Register your models here.
