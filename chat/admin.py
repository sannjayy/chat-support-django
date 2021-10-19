from django.contrib import admin
from .models import Chat

# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'is_seen', 'sent_at']
    list_per_page = 20