from django.urls import path
from .views import chat_view, SendAPIView, GetMessagesView, chat_session_start, end_chat_view, agent_join_chat_view, ChatTemplateCreateView, ChatTemplateDeleteView, change_template_status, GetNotificationView

app_name = 'chat' 

urlpatterns = [
    path('start-conversation/', chat_session_start, name='chat_session_start'),   
    path('join-agent/<str:id>', agent_join_chat_view, name='agent_join_chat'),

    # Crud
    path('template/add/', ChatTemplateCreateView.as_view(), name="add_chat_template"),
    path('template/<pk>/delete', ChatTemplateDeleteView.as_view(), name="delete_chat_template"),
    path('template/<pk>/status', change_template_status, name="change_template_status"),

    # Ajax
    path('sendMessage', SendAPIView, name='sendMessage'),    
    path('getMessages/<str:id>', GetMessagesView, name='getMessages'),
    path('end-conversation/<str:id>', end_chat_view, name='end_chat'),

    path('getNotification', GetNotificationView, name='get_notifications'),

    path('<str:id>/', chat_view, name='chat_view'),
]