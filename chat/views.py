from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Chat
# Create your views here.

@login_required
def chat_page_view(request):
    return render(request, 'chat/chat.html')

@login_required
def SendAPIView(request):
    message = request.POST['message']
    print(message)
    new_message = Chat.objects.create(
        sender = request.user,
        receiver_id = 2,
        message=message, 
    )
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required
def GetMessagesView(request):
    all_messages = Chat.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
    messages = [{
            'id': message.id,
            'sender': message.sender.username,
            'receiver': message.receiver_id,
            'message': message.message,
            'is_mine': message.sender == request.user,
            'is_seen': message.is_seen,
            'sent_at': message.sent_at,
        } for message in all_messages]
    # print(list(all_messages.values()))
    # return JsonResponse({"messages":list(all_messages.values())})
    return JsonResponse({"messages":messages})