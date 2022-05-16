from django import forms
from django.forms import ModelForm


from tournoi.models import ListJoueur, TourDeJeu
from accounts.models import Account


class ListJoueurForm(forms.ModelForm):
    class Meta:
        model = ListJoueur
        fields = '__all__'

    joueur_id = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False
    )
    tourdejeu_id = forms.ModelChoiceField(
        queryset=TourDeJeu.objects.all(),
        required=False
    )
    

