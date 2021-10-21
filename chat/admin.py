from django.contrib import admin
from .models import Chat, ChatSession, ChatTemplate
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(Chat)
class ChatAdmin(ImportExportModelAdmin):
    list_display = ['sender', 'receiver', 'message', 'session', 'is_seen', 'sent_at']
    list_per_page = 20

@admin.register(ChatSession)
class ChatSessionAdmin(ImportExportModelAdmin):
    list_display = ['user', 'agent', 'session', 'is_closed', 'created_at', 'updated_at']
    list_per_page = 20

@admin.register(ChatTemplate)
class ChatTemplateAdmin(ImportExportModelAdmin):
    list_display = ['user', 'message', 'status', 'created_at']
    list_per_page = 20