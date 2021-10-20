from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm # Set Password Dont Need Old Password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from chat.models import Chat, ChatSession, ChatTemplate
from .models import User


# Home Page View
class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        return super(HomePageView, self).get_context_data(**kwargs)


# Dashboard View
@login_required
def DashboardView(request):
    chat_templates = ChatTemplate.objects.filter(user = request.user)
    chat_sessions = ChatSession.objects.filter(is_closed=False)    
    context = {
        'chat_templates': chat_templates,
        'chat_sessions': chat_sessions,
    }
    return render(request, 'core/dashboard.html', context)

# Change Account Availability 
@login_required
def change_account_availability(request):
    user = User.objects.get(username = request.user.username)
    user.is_available = not user.is_available
    user.save()
    return redirect('core:dashboard')
    
# Authentication View
class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = "core/login.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super(LoginUser, self).dispatch(request, *args, **kwargs)
    

# Password Change View
@login_required
def user_change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed Successfully!')
            return redirect('core:home')

    return render(request, 'core/account_change_password.html' , { 'form': form})