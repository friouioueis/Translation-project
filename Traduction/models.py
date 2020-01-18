from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Create your models here.

LANGUAGE_CHOICES = (
    ('Ar', 'Arabe'),
    ('Fr', 'Francais'),
    ('An', 'Anglais'),
    ('Es', 'Espagnol'),
    ('It', 'Italien'),
    ('Al', 'Allmand'),
    ('Ch', 'Chinois'),
    ('Tu', 'Turque'),
    ('Kr', 'Koréen'),
    ('Rs', 'Russe')
)
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Nom', 'Prénom', 'username']
    is_client = models.BooleanField('client status', default=False)
    is_translator = models.BooleanField('translator status', default=False)
    Nom = models.CharField(max_length=50)
    Prénom = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    Wilaya = models.CharField(max_length=20)
    Commune = models.CharField(max_length=20)
    Adresse = models.CharField(max_length=100)
    Telephone = models.CharField(max_length=10)
    Fax = models.CharField(max_length=20)
    def __str__(self):
        return self.Nom + ' ' + self.Prénom
    class Meta:
        db_table = 'auth_user'


