from django.db import models
from django.utils import timezone
from datetime import datetime

from accounts.models import Account

# Create your models here.

class Ligue(models.Model):
    nom_ligue = models.CharField(max_length=30)

    class Meta:
        ordering = ('nom_ligue',)

    def __str__(self):
        return self.nom_ligue


class Club(models.Model):
    nom_club = models.CharField(max_length=30)
    short_name = models.CharField(max_length=5)
    ligue = models.ForeignKey(Ligue, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.nom_club

    class Meta:
        ordering = ('ligue__nom_ligue', 'short_name')


class ModeJeux(models.Model):
    mode_jeux = models.CharField('Mode de jeu',blank=True, null=True, max_length=30)
    color = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Mode de Jeux"

    def __str__(self):
        return self.mode_jeux

    @classmethod
    def get_default_pk(cls):
        modedejeu, created = cls.objects.get_or_create(
            mode_jeux='Pas de Tournoi', defaults=dict(color='FFFFFF'))
        return modedejeu.pk


class TourDeJeu(models.Model):
    tour_nbr = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Tour N°')
    lieu_organisation = models.ForeignKey(Club, on_delete=models.PROTECT)
    mode_jeu = models.ForeignKey(ModeJeux, default=ModeJeux.get_default_pk, blank=True, null=True, verbose_name='Mode de jeu', on_delete=models.PROTECT)
    nbr_maxi_joueur = models.PositiveSmallIntegerField(default=8, blank=True, null=True, verbose_name='Nombre maxi de joueur')
    nbr_inscrit = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name="Nombre d'inscrit")
    nbr_inscrit_att = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name="Nombre d'inscrit sur liste d'attente")
    date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name_plural = "Tour de Jeux"
        ordering = ('date', 'lieu_organisation__short_name')

    def __str__(self):
        return str(self.mode_jeu) + ' ' + str(self.lieu_organisation)


class ListJoueur(models.Model):
    joueur_id = models.ForeignKey(Account, blank=True, null=True, on_delete=models.PROTECT)
    tourdejeu_id = models.ForeignKey(TourDeJeu, blank=True, null=True, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True , blank=True)
    list_att = models.BooleanField(default=0, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Liste des joueurs par tournoi"
        ordering = ('date',)