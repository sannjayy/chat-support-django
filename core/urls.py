from django.urls import path
from .views import HomePage, LoginUser, user_change_password
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

app_name = 'core' 
auth_params = ''
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path(f'{auth_params}login/', LoginUser.as_view(), name='login'),
    path(f'{auth_params}logout/', LogoutView.as_view(), name='logout'),
    path(f'{auth_params}change-password/', user_change_password, name='change_password'),
]