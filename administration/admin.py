from django.contrib import admin
from .models import Saison

# Register your models here.
class SaisonAdmin(admin.ModelAdmin):
    model = Saison
    list_display = ['nom_saison', 'date_debut', 'date_fin', 'default']

admin.site.register(Saison, SaisonAdmin)
