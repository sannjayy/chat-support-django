from django.urls import path
from .views import chat_view, SendAPIView, GetMessagesView, chat_session_start, end_chat_view

app_name = 'chat' 

urlpatterns = [
    path('start-conversation/', chat_session_start, name='chat_session_start'),
    path('sendMessage', SendAPIView, name='sendMessage'),
    path('getMessages/<str:id>', GetMessagesView, name='getMessages'),
    path('end-conversation/<str:id>', end_chat_view, name='end_chat'),
    
    path('<str:id>/', chat_view, name='chat_view'),
]