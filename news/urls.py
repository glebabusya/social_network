from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.NewsView.as_view(), name='news'),
    path('/add-note', views.AddNoteView.as_view(), name='add_note'),
    path('/', include('registration.urls')),
    path('/', include('account.urls')),

]
