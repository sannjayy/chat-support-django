from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatSession, ChatTemplate
from core.models import User
import time
from .forms import ChatTemplateForm
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


# Chat View 
@login_required
def chat_view(request, id):
    # session = get_object_or_404(ChatSession, session=id)
    chat_templates = ChatTemplate.objects.filter(user=request.user).filter(status=True)
    try:
        session = ChatSession.objects.get(session=id, is_closed=False)
        if session:
            return render(request, 'chat/chat.html', context={'session':session, 'chat_templates':chat_templates})
    except:
        messages.warning(request, 'Chat session has been expired!')
        return redirect('chat:chat_session_start')


# Chat End View
@login_required
def end_chat_view(request, id):
    # session = get_object_or_404(ChatSession, session=id)
    try:
        # Get the chat session and close
        session = ChatSession.objects.get(session=id, is_closed=False)

        if request.user.is_staff: # If agent is rejecting
            session.agent = request.user
        session.is_closed=True
        session.save()

        # Make the agent Available
        user = User.objects.get(username = session.agent.username)
        user.is_available = True
        user.save()

        # Send a Exit Message
        Chat.objects.create(
            sender=request.user,
            receiver_id=session.user_id,
            session=session,
            message='<p style="color:red; font-weight:bold">left the chat</p>',
        )


        if session and request.user.is_staff:
            return redirect('core:dashboard')
        if session:
            return redirect('core:home')
    except:
        # return HttpResponse('Invalid Request!')
        messages.warning(request, 'Session has been closed!')
        return redirect('chat:chat_session_start')



@login_required
def agent_join_chat_view(request, id):
    # session = get_object_or_404(ChatSession, session=id)
    try:
        session = ChatSession.objects.get(session=id, is_closed=False, is_agent_joined=False)
        session.agent=request.user
        session.is_agent_joined=True
        session.save()
        user = User.objects.get(username = request.user.username)
        user.is_available = False
        user.save()
        if session and request.user.is_staff:
            Chat.objects.create(
                sender = request.user,
                receiver_id = session.user_id,
                session = session,
                message = f'Hello, I\'m {request.user.nickname}, how may I help you today?', 
            )
            return redirect('chat:chat_view', id=session.session)
    except:
        return HttpResponse('Invalid Request!')


# Chat Session Start View
@login_required
def chat_session_start(request):
    if request.method == 'POST' and not request.user.is_staff:
        # Find a available Agenet
        # agent = User.objects.filter(is_available=True, is_staff=True).order_by('?').first()
        # print(agent)
        # if not agent:
        #     return render(request, 'chat/chat_start.html', context={'message':'All agents are busy right now, please try after sometime...'})
        # Create a new chat session

        # Close all Previous Chat Sessions
        old_chat_sessions = ChatSession.objects.filter(user=request.user)
        for old_session in old_chat_sessions:
            old_session.is_closed = True
            old_session.save()

        # Create New session
        new_chat_session = ChatSession.objects.create(
            user = request.user,
            # agent = agent,
        )
        time.sleep(1)
        return redirect('chat:chat_view', id=new_chat_session.session)
    # Redirect to chat page
    return render(request, 'chat/chat_start.html')


# Send Msg Api View (Ajax)
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
        time.sleep(0.3)
    return HttpResponse('Message sent successfully')


# Receive Messages Api View
@login_required
def GetMessagesView(request, id):
    all_messages = Chat.objects.filter(session__session = id)
    messages = [{
            'id': message.id,
            'sender': message.sender.nickname,
            'receiver': message.receiver_id,
            'message': message.message,
            'is_mine': message.sender == request.user,
            'is_seen': message.is_seen,
            'sent_at': message.when_sent,
        } for message in all_messages]
    # print(list(all_messages.values()))
    # return JsonResponse({"messages":list(all_messages.values())})
    return JsonResponse({"messages":messages})


# Notification Api View
@login_required
def GetNotificationView(request):
    chat_sessions = ChatSession.objects.filter(is_agent_joined=False, is_closed=False)
    # messages = [{
    #         'id': message.id,
    #         'sender': message.sender.nickname,
    #         'receiver': message.receiver_id,
    #         'message': message.message,
    #         'is_mine': message.sender == request.user,
    #         'is_seen': message.is_seen,
    #         'sent_at': message.sent_at,
    #     } for message in all_messages]
    # print(list(all_messages.values()))
    return JsonResponse({"notifications":list(chat_sessions.values())})
    # return JsonResponse({"messages":messages})

# Add Chat Template
class ChatTemplateCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ChatTemplate
    template_name="chat/add_chat_template.html"
    form_class = ChatTemplateForm
    success_url = reverse_lazy('core:dashboard')
    success_message = "Template was created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Delete Chat Template
class ChatTemplateDeleteView(DeleteView):
    model = ChatTemplate
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('core:dashboard')

# Change Template Status
def change_template_status(request, pk):
    template = ChatTemplate.objects.get(id = pk, user=request.user)
    template.status = not template.status
    template.save()
    return redirect('core:dashboard')