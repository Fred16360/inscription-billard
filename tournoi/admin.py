from django.contrib import admin
from .models import Club, Ligue, ModeJeux, TourDeJeu, ListJoueur
# Register your models here.

class LigueAdmin(admin.ModelAdmin):
    model = Ligue
    list_display = ['nom_ligue']

admin.site.register(Ligue, LigueAdmin)


class ClubAdmin(admin.ModelAdmin):
    model = Club
    list_display = ['nom_club', 'short_name', 'ligue']


admin.site.register(Club, ClubAdmin)


class ModeJeuxAdmin(admin.ModelAdmin):
    model = ModeJeux
    list_display = ['mode_jeux', 'color']


admin.site.register(ModeJeux, ModeJeuxAdmin)


class TourDeJeuAdmin(admin.ModelAdmin):
    model = TourDeJeu
    ordering = ('tour_nbr', '-date')
    list_display = ['tour_nbr', 'lieu_organisation', 'mode_jeu', 'nbr_maxi_joueur', 'date']
    list_filter = ['mode_jeu', 'date']


admin.site.register(TourDeJeu, TourDeJeuAdmin)


class ListJoueurAdmin(admin.ModelAdmin):
    model = ListJoueur
    ordering = ('date',)
    list_display = ['date', 'joueur_id']


admin.site.register(ListJoueur, ListJoueurAdmin)