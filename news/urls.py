from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.NewsView.as_view(), name='news'),
    path('/', include('registration.urls')),
    path('/', include('account.urls'))

]
