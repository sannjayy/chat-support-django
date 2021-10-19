from django.urls import path
from .views import chat_page_view, SendAPIView, GetMessagesView

app_name = 'chat' 

urlpatterns = [
    path('', chat_page_view, name='start_chat'),
    path('sendMessage', SendAPIView, name='sendMessage'),
    path('getMessages/', GetMessagesView, name='getMessages'),
]