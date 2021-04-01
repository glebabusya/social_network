from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('logout', LogoutView.as_view(next_page='/facebook'), name='logout'),
    path('<str:name>', views.ProfileView.as_view(), name='profile'),
    path('<str:name>/redact', views.RedactProfileView.as_view(), name='redact'),
    path('<str:name>/<operation>', views.change_friends, name='add_friend'),

]
