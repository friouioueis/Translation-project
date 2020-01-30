from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
# Create your models here.

TRADUCTION_CHOIX = (
    ('General', 'General'),
    ('Scientifque', 'Scientifque'),
    ('Web', 'Web')
)

class Language(models.Model):
    title = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.title

class Note(models.Model):
    note = models.FloatField(default=0)
    def __str__(self):
        return str(self.note)

class User(AbstractUser):
    is_blocked = models.BooleanField(default=False)
    is_client = models.BooleanField('client status', default=False)
    cv = models.FileField(null=True, upload_to='files/cvs/', blank=True)
    is_translator = models.BooleanField('translator status', default=False)
    is_assermented = models.BooleanField(default=False)
    assertmente = models.FileField(null=True, blank=True, upload_to='files/assermente/')
    Nom = models.CharField(max_length=50)
    Prénom = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    languages = models.ManyToManyField(Language, blank=True)
    Wilaya = models.CharField(max_length=20)
    Commune = models.CharField(max_length=20)
    Adresse = models.CharField(max_length=100)
    Telephone = models.CharField(max_length=20)
    Fax = models.CharField(max_length=20)
    type = models.CharField(choices=TRADUCTION_CHOIX, max_length=11, blank=True)
    notes = models.ManyToManyField(Note, blank=True)

    def get_note(self):
        count = 0
        for note in self.notes.all():
            count = count + note.note
        i = self.notes.count()
        if i == 0:
            return 0
        else:
            return count/i
    def __str__(self):
        if self.is_superuser:
            return self.username
        return self.Nom + ' ' + self.Prénom
    class Meta:
        db_table = 'auth_user'

class Article(models.Model):
    title = models.CharField(max_length=20)
    Description = models.TextField()
    image = models.ImageField(null=True, upload_to='images/')
    def __str__(self):
        return self.title


class Devis(models.Model):
    is_done = models.BooleanField(default=False)
    fichi_trad = models.FileField(null=True, upload_to="files/Traduisé/")
    is_demanded = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    is_valid = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    client = models.CharField(max_length=20)
    traducteur = models.ManyToManyField(User)
    nom = models.CharField(max_length=20, null=True)
    prenom = models.CharField(max_length=20, null=True)
    mail = models.EmailField(max_length=255, null=True)
    adresse = models.CharField(max_length=100, null=True)
    langues = models.ManyToManyField(Language)
    type = models.CharField(choices=TRADUCTION_CHOIX, max_length=11, null=True)
    Zone = models.TextField(max_length=300, null=True)
    fichier = models.FileField(null=False, upload_to="files/Traduction/")
    def __str__(self):
        return 'Demande: '+self.nom +' '+self.prenom + ' de type :' + self.type
    class Meta:
        verbose_name_plural = 'Devis'
    def client_name(self):
        return User.objects.get(username=self.client).Prénom + ' ' + User.objects.get(username=self.client).Nom
    def client_email(self):
        return User.objects.get(username=self.client).email


