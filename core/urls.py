from django.urls import path
from django.views.generic import TemplateView
from .views import HomePageView, LoginUser, user_change_password, DashboardView, change_account_availability

from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

app_name = 'core' 
auth_params = 'auth/'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('payment/', TemplateView.as_view(template_name = 'core/payment.html'), name='payment'),


    path('action/change/visibility', change_account_availability, name="change_visibility_status"),
    # Auth
    path(f'{auth_params}login/', LoginUser.as_view(), name='login'),
    path(f'{auth_params}logout/', LogoutView.as_view(), name='logout'),
    path(f'{auth_params}change-password/', user_change_password, name='change_password'),
]