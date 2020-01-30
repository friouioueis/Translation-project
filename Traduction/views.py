from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from .models import User
from django.contrib import messages
from django.shortcuts import render
from .models import Language, Article, Devis, Note
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    context = {
        'langues': Language.objects.all,
        'articles': Article.objects.all,
        'traducteurs': User.objects.filter(is_translator=True),
        'traducteurs_assert': User.objects.filter(is_translator=True, is_assermented=True),
        'trad_gen': User.objects.filter(is_translator=True, type='General'),
        'trad_sci': User.objects.filter(is_translator=True, type='Scientifque'),
        'trad_web': User.objects.filter(is_translator=True, type='Web')
    }
    if request.user.is_superuser:
        return redirect('Traduction:admin_login')
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
    if request.user.is_superuser:
        return redirect('Traduction:admin_login')
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
    if request.user.is_superuser:
        return redirect('Traduction:admin_login')
    return redirect('Traduction:home')

def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_blocked is False:
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
        if user.is_blocked is True:
            messages.warning(request, "Voues étes bloqués pour le moment")
        else:
            messages.warning(request, "Utilisateur n'existe pas")
        return redirect('Traduction:home')

@login_required
def Logout(request):
    if request.user.is_superuser:
        logout(request)
        messages.info(request, 'Deconnexion avec succés')
        return redirect('Traduction:admin_login')
    else:
        logout(request)
        messages.info(request, 'Deconnexion avec succés')
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
    for i in range(len(traducteurs)):
        devis = Devis.objects.create(client=user, prenom=prenom, nom=nom, mail=mail, adresse=adresse, type=type_trad,
                                     fichier=fichier, Zone=zone)
        devis.traducteur.add(User.objects.filter(username=traducteurs[i])[0])
        devis.save()
        for j in range(len(langues)):
            devis.langues.add(Language.objects.filter(title=langues[j])[0])
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
        'devis': Devis.objects.filter(client=request.user.username, is_demanded=False),
        'trads': Devis.objects.filter(client=request.user.username, is_valid=True, is_approved=True, is_demanded=True)
    }
    return render(request, 'profils/client.html', context)


def Traducteur_profil(request):
    context = {
        'devis': Devis.objects.filter(is_approved=False, traducteur=request.user, is_valid=True),
        'trads': Devis.objects.filter(is_approved=True, traducteur=request.user, is_valid=True, is_demanded=True, is_done=False),
        'langues': Language.objects.all
    }
    return render(request, 'profils/traducteur.html', context)

@login_required
def modify_account(request):
    username = request.POST.get('Username')
    password = request.POST.get('Password')
    nom = request.POST.get('Nom')
    prenom = request.POST.get('Prénom')
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
    request.user.Prénom = prenom
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

@login_required
def modify_translator(request):
    name = request.POST.get('Nom')
    prenom = request.POST.get('Prénom')
    username = request.POST.get('Username')
    email = request.POST.get('Mail')
    password = request.POST.get('Password')
    language = request.POST.getlist('language')
    type_trad = request.POST.get('type')
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    assermente = request.POST.get('assermente')
    if assermente == 'True':
        is_assermente = True
        assermente_file = request.FILES['fichier_assert']
        request.user.is_assermented = True
        request.user.assertmente = assermente_file
        assermente_file = True
    else:
        if assermente == 'False':
            request.user.is_assermented = False
        assermente_file = False
    fax = request.POST.get('Fax')
    if username != request.user.username and User.objects.filter(username=username).exists():
        messages.warning(request, "Cet utilisateur déjà existe")
        return redirect('Traduction:traducteur_profil')
    else:
        request.user.username = username
        request.user.save()
    request.user.Nom = name
    request.user.Prénom = prenom
    request.user.email = email
    request.user.Telephone = telephone
    request.user.Fax = fax
    request.user.Wilaya = wilaya
    request.user.Commune = commune
    request.user.Adresse = adresse
    request.user.save()
    if password != '':
        request.user.set_password(password)
        request.user.save()
    if len(request.FILES) > 1 and assermente_file is True:
         cv = request.FILES['cv']
         request.user.cv = cv
         request.user.save()
    if len(request.FILES) > 0 and assermente_file is False:
         cv = request.FILES['cv']
         request.user.cv = cv
         request.user.save()
    if type_trad is not None:
        request.user.type = type_trad
        request.user.save()
    if len(language) != 0:
        request.user.languages.clear()
        for i in range(len(language)):
            request.user.languages.add(Language.objects.filter(title=language[i])[0])
    messages.info(request, "Profil modifié avec succés")
    login(request, request.user)
    return redirect('Traduction:traducteur_profil')

@login_required
def delete_devis(request, pk):
    devis = Devis.objects.get(id=pk)
    devis.delete()
    messages.info(request, "Le devis a été bien supprimé")
    return redirect('Traduction:client_profil')

@login_required
def approve_devis(request, pk):
    prix = request.POST.get('price')
    devis = Devis.objects.get(id=pk)
    devis.price = prix
    devis.is_approved = True
    devis.save()
    messages.info(request, "Devis approuvé")
    return redirect('Traduction:traducteur_profil')

@login_required
def supprimer_devis(request, pk):
    devis = Devis.objects.get(id=pk)
    devis.price = 0
    devis.is_valid = False
    devis.save()
    messages.warning(request, "Devis refusé")
    return redirect('Traduction:traducteur_profil')


@login_required
def demand_trad(request, pk):
    devis = Devis.objects.get(id=pk)
    devis.is_demanded = True
    devis.save()
    messages.info(request, "Demande de traduction envoyé")
    return redirect('Traduction:client_profil')

@login_required
def envoyer_trad(request, pk):
    fichi = request.FILES['Traduise']
    devis = Devis.objects.get(id=pk)
    devis.fichi_trad = fichi
    devis.is_done = True
    devis.save()
    messages.info(request, "Votre fichier a bien été envoyé")
    return redirect('Traduction:traducteur_profil')

@login_required
def noter_trad(request, pk):
    noter = request.POST.get('note')
    note = Note.objects.create(note=noter)
    devis = Devis.objects.get(id=pk)
    for trad in devis.traducteur.all():
        trad.notes.add(note)
        trad.save()
    messages.info(request, "votre note est envoyé au traducteur")
    return redirect('Traduction:client_profil')

def admin_login_custom(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_superuser:
            login(request, user)
            messages.info(request, "Bienvenue")
            return redirect('Traduction:admin_login')
        else:
            messages.warning(request, "Vous n'étes pas un admin")
            return redirect('Traduction:home')
    else:
        messages.warning(request, "Cet utilisateur n'existe pas")
        return redirect('Traduction:admin_login')

def admin_page(request):
    context = {
        'clients': User.objects.filter(is_client=True),
        'traducteurs': User.objects.filter(is_translator=True),
        'langues': Language.objects.all
    }
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'admin/admin_page.html', context)
    if request.user.is_authenticated is False:
        return render(request, 'admin/login_page.html')
    if request.user.is_authenticated and request.user.is_superuser is False:
        messages.warning(request, "Vous n'étes pas un admin")
        return redirect('Traduction:home')

def block_user(request, pk):
    user = User.objects.get(username=pk)
    if user.is_blocked:
        user.is_blocked = False
        user.save()
    else:
        user.is_blocked = True
        user.save()
    return redirect('Traduction:admin_login')
def admin_modify(request, pk):
    context = {
        'user': User.objects.get(username=pk),
        'langues': Language.objects.all
    }
    return render(request, 'admin/admin_modify_user.html', context)


@login_required
def modify_admin_client(request, pk):
    user = User.objects.get(username=pk)
    username = request.POST.get('Username')
    password = request.POST.get('Password')
    nom = request.POST.get('Nom')
    prenom = request.POST.get('Prénom')
    mail = request.POST.get('Mail')
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    fax = request.POST.get('Fax')
    if username != user.username and User.objects.filter(username=username).exists():
        messages.warning(request, "Cet utilisateur déjà existe")
        return redirect('Traduction:home')
    else:
        user.username = username
        user.save()
    user.Nom = nom
    user.Prénom = prenom
    user.email = mail
    user.Telephone = telephone
    user.Fax = fax
    user.Wilaya = wilaya
    user.Commune = commune
    user.Adresse = adresse
    user.save()
    if password != '':
        user.set_password(password)
        user.save()
    messages.info(request, "Client modifié avec succés")
    return redirect('Traduction:admin_login')

def modify_admin_translator(request, pk):
    user = User.objects.get(username=pk)
    name = request.POST.get('Nom')
    prenom = request.POST.get('Prénom')
    username = request.POST.get('Username')
    email = request.POST.get('Mail')
    password = request.POST.get('Password')
    language = request.POST.getlist('language')
    type_trad = request.POST.get('type')
    wilaya = request.POST.get('Wilaya')
    commune = request.POST.get('Commune')
    adresse = request.POST.get('Adresse')
    telephone = request.POST.get('Telephone')
    assermente = request.POST.get('assermente')
    if assermente == 'True':
        is_assermente = True
        assermente_file = request.FILES['fichier_assert']
        user.is_assermented = True
        user.assertmente = assermente_file
        assermente_file = True
    else:
        if assermente == 'False':
            user.is_assermented = False
        assermente_file = False
    fax = request.POST.get('Fax')
    if username != user.username and User.objects.filter(username=username).exists():
        messages.warning(request, "Cet utilisateur déjà existe")
        return redirect('Traduction:admin_login')
    else:
        user.username = username
        user.save()
    user.Nom = name
    user.Prénom = prenom
    user.email = email
    user.Telephone = telephone
    user.Fax = fax
    user.Wilaya = wilaya
    user.Commune = commune
    user.Adresse = adresse
    user.save()
    if password != '':
        user.set_password(password)
        user.save()
    if len(request.FILES) > 1 and assermente_file is True:
        cv = request.FILES['cv']
        user.cv = cv
        user.save()
    if len(request.FILES) > 0 and assermente_file is False:
        cv = request.FILES['cv']
        user.cv = cv
        user.save()
    if type_trad is not None:
        user.type = type_trad
        user.save()
    if len(language) != 0:
        user.languages.clear()
        for i in range(len(language)):
            user.languages.add(Language.objects.filter(title=language[i])[0])
    messages.info(request, "Traducteur modifié avec succés")
    return redirect('Traduction:admin_login')
