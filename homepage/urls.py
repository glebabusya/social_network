from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    # path('/test', views.TestingPage.as_view(), name='test')

]
