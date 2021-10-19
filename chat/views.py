from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatSession
from core.models import User
import time

# Create your views here.



@login_required
def chat_view(request, id):
    # session = get_object_or_404(ChatSession, session=id)
    try:
        session = ChatSession.objects.get(session=id, is_closed=False)
        if session:
            return render(request, 'chat/chat.html', context={'session':session})
    except:
        return HttpResponse('Chat session has been expired!')


@login_required
def end_chat_view(request, id):
    # session = get_object_or_404(ChatSession, session=id)
    try:
        session = ChatSession.objects.get(session=id, is_closed=False)
        session.is_closed=True
        session.save()
        if session:
            return redirect('core:home')
    except:
        return HttpResponse('Invalid Request!')

@login_required
def chat_session_start(request):
    if request.method == 'POST':
        # Find a available Agenet
        agent = User.objects.filter(is_available=True, is_staff=True).order_by('?').first()
        # print(agent)
        if not agent:
            return render(request, 'chat/chat_start.html', context={'message':'All agents are busy right now, please try after sometime...'})
        # Create a new chat session
        new_chat_session = ChatSession.objects.create(
            user = request.user,
            agent = agent,
        )
        time.sleep(1)
        return redirect('chat:chat_view', id=new_chat_session.session)
    # Redirect to chat page
    return render(request, 'chat/chat_start.html')


@login_required
def SendAPIView(request):
    message = request.POST['message']
    url = request.POST['url']
    
    session_id = url.rsplit('/', -1)[-2]
    session = get_object_or_404(ChatSession, session=session_id)
    new_message = Chat.objects.create(
        sender = request.user,
        receiver_id = session.agent_id,
        session = session,
        message = message, 
    )
    if message:
        new_message.save()
        time.sleep(0.5)
    return HttpResponse('Message sent successfully')

@login_required
def GetMessagesView(request, id):
    print(id)
    all_messages = Chat.objects.filter(session__session = id)
    messages = [{
            'id': message.id,
            'sender': message.sender.nickname,
            'receiver': message.receiver_id,
            'message': message.message,
            'is_mine': message.sender == request.user,
            'is_seen': message.is_seen,
            'sent_at': message.sent_at,
        } for message in all_messages]
    # print(list(all_messages.values()))
    # return JsonResponse({"messages":list(all_messages.values())})
    return JsonResponse({"messages":messages})