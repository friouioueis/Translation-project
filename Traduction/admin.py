from django.contrib import admin
from .models import User, Language, Devis, Article

# Register your models here.
admin.site.register(User)
admin.site.register(Language)
admin.site.register(Devis)
admin.site.register(Article)



