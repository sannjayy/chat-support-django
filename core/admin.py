from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission

from .models import User
from .forms import UserChangeForm, UserCreationForm

# Admin Dashboard Texts
admin.site.site_header = "Customer Support Admin"
admin.site.site_title = "Customer Support Admin Portal"
admin.site.index_title = "Welcome to Customer Support"

# User Admin
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    # List admin
    list_display = ('username', 'email', 'full_name', 'is_email_verified', 'is_available', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_email_verified', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'is_email_verified', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','mobile', 'whatsapp',)}),
        ('Permissions', {'fields': ('is_available', 'is_active', 'is_staff', 'is_superuser', 'groups')}), # 'user_permissions', 'groups'
    )
    # Creating new user from admin
    add_fieldsets = (
        ('User Information', {'classes': ('wide',), 'fields': ('first_name', 'last_name', 'mobile', 'whatsapp', 'email', 'username', 'password1', 'password2',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        
    )
    search_fields = ('email', 'first_name', 'username')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups',)
    list_per_page = 10


# User Admin Register
admin.site.register(User, UserAdmin)
admin.site.register(Permission)
