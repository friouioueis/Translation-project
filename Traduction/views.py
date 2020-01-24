from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from .models import User
from django.contrib import messages
from django.shortcuts import render
from .models import Language, Article, Devis
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    context = {
        'langues': Language.objects.all,
        'articles': Article.objects.all,
        'traducteurs': User.objects.filter(is_translator=True),
        'traducteurs_assert': User.objects.filter(is_translator=True, is_assermented=True)
    }
    return render(request, 'base.html', context)
def signUp(request):
    username = request.POST.get('Username')
    password = request.POST.get('Password')
    nom = request.POST.get('Nom')
    prénom = request.POST.get('Prénom')
    mail = request.POST.get('Mail')
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    fax = request.POST.get('Fax')
    if len(username) == 0:
        messages.warning(request, "Insérez un nom d'utilisateur")
        return redirect('Traduction:home')
    if len(password) == 0:
        messages.warning(request, "Insérez un mot de passe")
        return redirect('Traduction:home')
    if User.objects.filter(username=username).exists():
        messages.warning(request, "Cet utilisateur déjà existe")
        return redirect('Traduction:home')
    else:
        user = User.objects.create(username=username, Nom=nom, Prénom=prénom, email=mail, Wilaya=wilaya, Commune=commune, Adresse=adresse, Telephone=telephone, Fax=fax, is_client=True)
        user.set_password(password)
        user.save()
        messages.info(request, "Votre compte client a été créé")
    return redirect('Traduction:home')


def signUpTraducteur(request):
    username = request.POST.get('Username')
    password = request.POST.get('Password')
    cv = request.FILES['cv']
    nom = request.POST.get('Nom')
    prénom = request.POST.get('Prénom')
    mail = request.POST.get('Mail')
    trad_type = request.POST.get('type')
    assermente = request.POST.get('assermente')
    if assermente == 'True':
        is_assermente = True
        assermente_file = request.FILES['fichier_assert']
    else:
        is_assermente = False
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    fax = request.POST.get('Fax')
    langues = request.POST.getlist('language')
    if len(username) == 0:
        messages.warning(request, "Insérez un nom d'utilisateur")
        return redirect('Traduction:home')
    if len(password) == 0:
        messages.warning(request, "Insérez un mot de passe")
        return redirect('Traduction:home')
    if User.objects.filter(username=username).exists():
        messages.warning(request, "Cet utilisateur déjà existe")
        return redirect('Traduction:home')
    else:
        if is_assermente:
            user = User.objects.create(username=username, type=trad_type, Nom=nom, Prénom=prénom, email=mail, Wilaya=wilaya,
                                       Commune=commune, Adresse=adresse, Telephone=telephone, Fax=fax, is_translator=True,
                                       is_assermented=is_assermente, assertmente=assermente_file, cv=cv)
        else:
            user = User.objects.create(username=username, type=trad_type, Nom=nom, Prénom=prénom, email=mail, Wilaya=wilaya,
                                       Commune=commune, Adresse=adresse, Telephone=telephone, Fax=fax, is_translator=True,
                                       is_assermented=is_assermente, cv=cv)
        user.set_password(password)
        user.save()
        for i in range(len(langues)):
            user.languages.add(Language.objects.filter(title=langues[i])[0])
            user.save()
        messages.info(request, "Votre compte traducteur a été créé")
    return redirect('Traduction:home')

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.is_client:
            messages.info(request, "Client authentifié")
            return redirect('Traduction:home')
        if user.is_translator:
            messages.info(request, "Traducteur authentifié")
            return redirect('Traduction:home')
        messages.info(request, "Bonjour Superuser!")
        return redirect('Traduction:home')
    else:
        messages.warning(request, "Utilisateur n'existe pas")
        return redirect('Traduction:home')

@login_required
def Logout(request):
    logout(request)
    messages.info(request,'Deconnexion avec succés')
    return redirect('Traduction:home')


def recrut(request):
    context = {
        'langues': Language.objects.all,
        'articles': Article.objects.all
    }
    return render(request, 'recrutement.html', context)
def blog(request):
    context = {
        'langues': Language.objects.all,
        'articles': Article.objects.all
    }
    return render(request, 'blog.html', context)

@login_required
def add_devis(request):
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    mail = request.POST.get('mail')
    adresse = request.POST.get('adresse')
    traducteurs = request.POST.getlist('traducteur')
    langues = request.POST.getlist('language')
    type_trad = request.POST.get('type')
    fichier = request.FILES['fichier']
    zone = request.POST.get('zone')
    user = request.user.username
    devis = Devis.objects.create(client=user, prenom=prenom, nom=nom, mail=mail, adresse=adresse, type=type_trad, fichier=fichier, Zone=zone)
    for i in range(len(traducteurs)):
        devis.traducteur.add(User.objects.filter(username=traducteurs[i])[0])
        devis.save()
    for i in range(len(langues)):
        devis.langues.add(Language.objects.filter(title=langues[i])[0])
        devis.save()
    messages.info(request, "votre devis a été créé")
    if request.user.is_client:
        return redirect('Traduction:client_profil')
    if request.user.is_translator:
        return redirect('Traduction:traducteur_profil')

def about(request):
    return render(request, 'about.html')

def traducteurs(request):
    context = {
        'traducteurs': User.objects.filter(is_translator=True)
    }
    return render(request, 'traducteurs.html', context)

def client_profil(request):
    context = {
        'devis': Devis.objects.filter(client=request.user.username)
    }
    return render(request, 'profils/client.html', context)


def Traducteur_profil(request):
    return render(request, 'profils/traducteur.html')

@login_required
def modify_account(request):
    username = request.POST.get('Username')
    password = request.POST.get('Password')
    nom = request.POST.get('Nom')
    prénom = request.POST.get('Prénom')
    mail = request.POST.get('Mail')
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    fax = request.POST.get('Fax')
    if username != request.user.username and User.objects.filter(username=username).exists():
        messages.warning(request, "Cet utilisateur déjà existe")
        return redirect('Traduction:client_profil')
    else:
        request.user.username = username
        request.user.save()
    request.user.Nom = nom
    request.user.Prénom = prénom
    request.user.email = mail
    request.user.Telephone = telephone
    request.user.Fax = fax
    request.user.Wilaya = wilaya
    request.user.Commune = commune
    request.user.Adresse = adresse
    request.user.save()
    if password != '':
        request.user.set_password(password)
        request.user.save()
    messages.info(request, "Profil modifié avec succés")
    login(request, request.user)
    return redirect('Traduction:client_profil')

def modify_translator(request):
    pass