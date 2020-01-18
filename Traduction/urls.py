from django.urls import path, include
from django.contrib.auth.views import LoginView
from . import views

app_name = "Traduction"

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signUp, name='Signup'),
    path('login/', views.Login, name='Login')
]