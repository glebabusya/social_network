from django.urls import path, include
from . import views

urlpatterns = [
    path('/', views.NewsView.as_view(), name='news'),
    path('/add-note', views.AddNoteView.as_view(), name='add_note'),
    path('/delete_note/<int:note_pk>/<str:back_url>/<str:username>', views.delete_note, name='delete_note'),
    path('/comment/<int:note_pk>/<str:back_url>/<str:username>', views.change_comment, name='comment'),
    path('/like/<int:note_pk>/<str:back_url>/<str:username>', views.like, name='like'),
    path('/like/<int:note_pk>/<str:back_url>/<int:note_id>/<str:url>/<str:name>', views.like, name='like2'),
    path('/note/<int:note_id>/<str:url>/<str:name>', views.NoteView.as_view(), name='note'),
    path('/', include('registration.urls')),
    path('/', include('account.urls')),

]
