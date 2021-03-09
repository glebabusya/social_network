from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:username>', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/redact', views.RedactProfileView.as_view(), name='redact'),
    path('<str:username>/<operation>', views.change_friends, name='add_friend')
]
