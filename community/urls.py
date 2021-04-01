from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('create_group', views.CreateGroupView.as_view(), name='create_group'),
    path('subscribe/<str:name>', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:name>', views.unsubscribe, name='unsubscribe'),
    path('redact_group/<str:name>', views.RedactGroupView.as_view(), name='redact_group'),
    path('<str:name>', views.GroupView.as_view(), name='group'),
]
