from django.db import models

# Create your models here.
class Saison(models.Model):
    nom_saison = models.CharField(max_length=50, blank=True)
    date_debut = models.DateField(auto_now=False, auto_now_add=False)
    date_fin = models.DateField(auto_now=False, auto_now_add=False)
    default = models.BooleanField()