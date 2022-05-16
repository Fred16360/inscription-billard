from django import forms
from django.forms import ModelForm
from . import models

from tournoi.models import ListJoueur, ModeJeux, TourDeJeu, Club
from administration.models import Saison


class TourdejeuForm(forms.ModelForm):
    class Meta:
        model = TourDeJeu
        fields = '__all__'

    tour_nbr = forms.IntegerField(
        required=False,
        label="Tour N° ",
        widget=forms.NumberInput(attrs={
            "class":"form-check-input"
        })
    )
    lieu_organisation = forms.ModelChoiceField(
        queryset=Club.objects.all(),
        label="Club organisateur ",
        required=False,
        widget=forms.Select(attrs={
            "class":"form-select",
            "onfocus":"this.defaultIndex=this.selectedIndex;",
            "onchange":"this.selectedIndex=this.defaultIndex;"
        })
    )
    mode_jeu = forms.ModelChoiceField(
        queryset=ModeJeux.objects.all(),
        label="Mode de jeu ",
        required=False,
        widget=forms.Select(attrs={
            "class":"form-select"
        })
    )
    nbr_maxi_joueur = forms.IntegerField(
        required=False,
        label="Nombre maxi de joueurs",
        widget=forms.NumberInput(attrs={
            "class":"form-check-input"
        })
    )
    date = forms.DateField(
        required=False,
        label="Date du tournoi",
        widget=forms.DateInput(attrs={
            "class":"form-control",
            "readonly":"readonly"
        })
    )


class SaisonForm(forms.ModelForm):
    class Meta:
        model = Saison
        fields = '__all__'

    nom_saison = forms.CharField(
        label="Nom de la saison",
        required=True
    )
    date_debut = forms.DateField(
        label="1er Dimanche de Septembre",
        required=True
    )
    date_fin = forms.DateField(
        label="Dernier dimanche d'Août",
        required=True
    )
    default = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input"
        }) 
    )
