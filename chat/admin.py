from django.contrib import admin
from .models import Chat, ChatSession, ChatTemplate

# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'session', 'is_seen', 'sent_at']
    list_per_page = 20

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'agent', 'session', 'is_closed', 'created_at']
    list_per_page = 20

@admin.register(ChatTemplate)
class ChatTemplateAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'status', 'created_at']
    list_per_page = 20