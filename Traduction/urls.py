from django.urls import path, include
from django.contrib.auth.views import LoginView
from . import views

app_name = "Traduction"

urlpatterns = [
    path('', views.home, name='home'),
    path('client/signed-up/', views.signUp, name='Signup'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('traducteur/Signed-up/', views.signUpTraducteur, name='SignupTrad'),
    path('recrutement/', views.recrut, name='recrutement'),
    path('blog/', views.blog, name='blog'),
    path('devis/', views.add_devis, name='add_devis'),
    path('About', views.about, name='about'),
    path('Traducteurs', views.traducteurs, name='traducteurs'),
    path('profil/', views.client_profil, name='client_profil'),
    path('profil/client/modified', views.modify_account, name='modify-client'),
    path('profil/traducteur', views.Traducteur_profil, name='traducteur_profil'),
    path('profil/traducteur/modified', views.modify_translator, name='modify-traducteur')

]