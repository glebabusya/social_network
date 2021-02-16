from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('login', views.LoginView.as_view(), name='login'),
    path('recovery', views.AccountRecoveryView.as_view(), name='recovery'),
    path('password-change<str:hash>', views.ChangePasswordView.as_view(), name='password-change')

]
