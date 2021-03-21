from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('subscribe/<str:group_name>', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:group_name>', views.unsubscribe, name='unsubscribe'),
    path('redact_group/<str:group_name>', views.RedactGroupView.as_view(), name='redact_group'),
    path('<str:group_name>', views.GroupView.as_view(), name='group')
]
