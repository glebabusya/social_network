from django.urls import path, include
from community.views import GroupsView
from . import views

urlpatterns = [
    path('/', views.NewsView.as_view(), name='news'),
    path('/add-note/group/<str:name>', views.AddNoteView.as_view(), name='add_note'),
    path('/add-note/profile', views.AddNoteView.as_view(), name='add_note'),
    path('/delete_note/<int:note_pk>/<str:back_url>/<str:name>', views.delete_note, name='delete_note'),
    path('/comment/<int:note_pk>/<str:back_url>/<str:name>', views.change_comment, name='comment'),
    path('/like/<int:note_pk>/<str:back_url>/<str:name>', views.like, name='like'),
    path('/note/<int:note_id>/<str:url>/<str:name>', views.NoteView.as_view(), name='note'),
    path('/groups/', GroupsView.as_view(), name='groups'),
    path('/groups/<str:search>', GroupsView.as_view(), name='groups'),
    path('/group/', include('community.urls')),
    path('/', include('registration.urls')),
    path('/profile/', include('account.urls')),

]
