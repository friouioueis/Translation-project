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
    path('profil/traducteur/modified', views.modify_translator, name='modify-traducteur'),
    path('profil/client/remove_devis/<pk>', views.delete_devis, name='delete_devis'),
    path('profil/traducteur/approve_devis/<pk>', views.approve_devis, name='approve_devis'),
    path('profil/traducteur/refuse_devis/<pk>', views.supprimer_devis, name='refuse_devis'),
    path('profil/traducteur/envoyer_trad/<pk>', views.envoyer_trad, name='envoi_trad'),
    path('profil/client/demander_trad/<pk>', views.demand_trad, name='demand_trad'),
    path('profil/client/noter_trad/<pk>', views.noter_trad, name='noter_trad'),
    path('admin/loggedin/', views.admin_login_custom, name='admin_login_custom'),
    path('admin/', views.admin_page, name='admin_login'),
    path('admin/block_user/<pk>', views.block_user, name='block_user'),
    path('admin/modify_user/<pk>', views.admin_modify, name='admin_modify'),
    path('admin/modify_client/<pk>', views.modify_admin_client, name='admin_modify_client'),
    path('admin/modify_translator/<pk>', views.modify_admin_translator, name='admin_modify_translator')

]