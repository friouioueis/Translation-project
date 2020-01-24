from django import template
from Traduction.models import Devis, User

register = template.Library()

@register.filter
def devis_count(user):
    count = 0
    if user.is_client:
        qs = Devis.objects.filter(client=user.username)
    if user.is_translator:
        devis = Devis.objects.all()
        for devi in devis:
            if user in devi.traducteur.all():
                count = count+1
        return count
    return qs.count()