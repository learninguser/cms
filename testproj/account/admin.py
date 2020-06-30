from django.contrib import admin
from django.conf import settings
from django.contrib.auth import get_user_model
# from account.models import User
from django.contrib.auth.admin import UserAdmin
from account.forms import SignUpForm

class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'pic'),
        }),
    )

# Register your models here.
admin.site.register(get_user_model(), MyUserAdmin)