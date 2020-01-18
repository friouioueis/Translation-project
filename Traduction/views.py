from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .models import User
from django.contrib import messages
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'base.html')
def signUp(request):
    nom = request.POST.get('Nom')
    prénom = request.POST.get('Prénom')
    username = request.POST.get('Username')
    email = request.POST.get('Mail')
    password = request.POST.get('Password')
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    fax = request.POST.get('Fax')
    if (len(username) == 0) | (len(password) == 0) | (len(nom) == 0) | (len(prénom) == 0) | (len(email) == 0) | (len(wilaya) == 0) | (len(commune) == 0) | (len(adresse) == 0) | (len(telephone) == 0) | (len(fax) == 0):
        messages.warning(request, "Rempilssez tous les champs")
        return redirect('Traduction:home')
    if len(password) == 0:
        messages.warning(request, "Insérez un mot de passe")
        return redirect('Traduction:home')
    if User.objects.filter(email=email).exists():
        messages.warning(request, "Cet Email est déjà prit")
        return redirect('Traduction:home')
    else:
        user = User.objects.create(Nom=nom, Prénom=prénom,username=username, email=email, password=password, Wilaya=wilaya, Commune=commune, Adresse=adresse, Telephone=telephone, Fax=fax, is_client=True)
        user.save()
        messages.info(request, "Votre compte a été créé")
    return redirect('Traduction:home')

def Login(request):
    email = request.POST['Email']
    password = request.POST['Password']
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        messages.info(request, "Utilisateur authentifié")
        return redirect('Traduction:home')
    else:
        messages.warning(request, "Utilisateur n'existe pas")
        return redirect('Traduction:home')
