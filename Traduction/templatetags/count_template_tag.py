from django import template
from Traduction.models import Devis, User

register = template.Library()

@register.filter
def devis_count(user):
    count = 0
    if user.is_client:
        qs = Devis.objects.filter(client=user.username, is_demanded=False)
    if user.is_translator:
        devis = Devis.objects.all()
        for devi in devis:
            if user in devi.traducteur.all() and devi.is_approved is False and devi.is_valid is True:
                count = count+1
        return count
    return qs.count()

@register.filter
def trad_count(user):
    count = 0
    if user.is_client:
        qs = Devis.objects.filter(client=user.username, is_demanded=True)
    if user.is_translator:
        devis = Devis.objects.all()
        for devi in devis:
            if user in devi.traducteur.all() and devi.is_demanded is True and devi.is_done is False:
                count = count+1
        return count
    return qs.count()