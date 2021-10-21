from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
    list_display = ('username', 'email', 'nickname', 'is_available', 'is_staff', 'date_joined', 'last_login')
    list_filter = ('is_email_verified', 'is_staff', 'is_superuser')
    fieldsets = (        
        ('Personal info', {'fields': ('first_name', 'last_name','mobile', 'whatsapp',)}),
        ('User Credentials', {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}), # 'user_permissions', 'groups'
    )
    # Creating new user from admin
    add_fieldsets = (
        ('User Information', {'classes': ('wide',), 'fields': ('first_name', 'last_name', 'mobile', 'whatsapp', )}),
        ('User Credentials', {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        
    )
    search_fields = ('email', 'first_name', 'username')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups',)
    list_per_page = 10


# User Admin Register
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)