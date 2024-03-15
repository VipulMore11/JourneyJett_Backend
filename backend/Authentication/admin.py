from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'password', 'phone_no']

admin.site.register(User, UserAdmin)