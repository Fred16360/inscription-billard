from django.shortcuts import render, redirect
from django.db.models import Count
from datetime import datetime, date, timedelta, time

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Ligue, Club, ModeJeux, TourDeJeu, ListJoueur, Account
from tournoi.forms import ListJoueurForm
from administration.models import Saison
# Create your views here.


def inscription(request):
    list_ligue = Ligue.objects.all()
    list_club = Club.objects.all()
   # list_tourdejeu = TourDeJeu.objects.all().order_by('date', 'lieu_organisation__ligue__nom_ligue', 'lieu_organisation__short_name')
    saison = Saison.objects.filter(default=True).last()
 
    today = datetime.now()
    diff_start = 7 - (6 - today.weekday())
    diff_end = 42 - (6 - today.weekday())
    start = today - timedelta(diff_start)
    end = today + timedelta(diff_end)
    start_date = today.replace(hour=18, minute=00, second=00) - timedelta(diff_start)
    end_date = today.replace(hour=18, minute=00, second=00) + timedelta(diff_end)
    list_tourdejeu = TourDeJeu.objects.filter(date__range=[start, end]).order_by('date', 'lieu_organisation__ligue__nom_ligue', 'lieu_organisation__short_name')

    list_date = []
    tournoi_date = start_date
    while tournoi_date <= end_date:
        ouverture_date = tournoi_date - timedelta(23)
        fermeture_date = tournoi_date - timedelta(9)
        list_date.append({
            'tournoi_date': tournoi_date,
            'ouverture_date': ouverture_date,
            'fermeture_date':fermeture_date,
            'today':today
        })

        tournoi_date = tournoi_date + timedelta(7)

    return render(request, 'inscription.html', {
        'list_ligue': list_ligue,
        'list_club': list_club,
        'list_tourdejeu': list_tourdejeu,
        'list_date': list_date,
        'today':today,
        })


@login_required(login_url='../../accounts/login/')
def list_joueur(request, pk):
    joueur = request.user
    try:
        tourdejeu = TourDeJeu.objects.get(pk=pk)
    except TourDeJeu.DoesNotExist:
        return redirect('inscription')

    tdj_tournbr = tourdejeu.tour_nbr
    tdj_modejeu = tourdejeu.mode_jeu
    tdj = TourDeJeu.objects.filter(tour_nbr=tdj_tournbr).filter(mode_jeu=tdj_modejeu).values_list('pk', flat=True)

    joueur_inscrit = ListJoueur.objects.filter(joueur_id=joueur).filter(list_att=0).filter(tourdejeu_id__in=tdj)
    joueur_inscrit_att = ListJoueur.objects.filter(joueur_id=joueur).filter(list_att=1).filter(tourdejeu_id__in=tdj)
    date_inscrit = ListJoueur.objects.filter(tourdejeu_id=pk).filter(joueur_id=joueur).filter(list_att=0)
    date_inscrit_att = ListJoueur.objects.filter(tourdejeu_id=pk).filter(joueur_id=joueur).filter(list_att=1)

    nbr_inscrit = tourdejeu.nbr_inscrit
    nbr_inscrit_att = tourdejeu.nbr_inscrit_att
    nbr_joueur = tourdejeu.nbr_maxi_joueur
    nbr_joueur_att = tourdejeu.nbr_maxi_joueur + 3
     
    if joueur_inscrit.exists():
        inscrit = 1
    else:
        inscrit = 0

    if joueur_inscrit_att.exists():
        inscrit_att = 1
    else:
        inscrit_att = 0

    if date_inscrit.exists():
        inscrit_day = 1
    else:
        inscrit_day = 0

    if date_inscrit_att.exists():
        inscrit_day_att = 1
    else:
        inscrit_day_att = 0


    list = ListJoueur.objects.filter(tourdejeu_id=pk).filter(list_att=0)
    list_att = ListJoueur.objects.filter(tourdejeu_id=pk).filter(list_att=1)

    form = ListJoueurForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, "list_joueur.html", {
        'list_joueur': list,
        'list_joueur_att': list_att, 
        'ref_pk': pk, 
        'inscrit': inscrit, 
        'tdj': joueur_inscrit_att,
        'inscrit_att': inscrit_att,
        'inscrit_day': inscrit_day,
        'inscrit_day_att': inscrit_day_att,
        'nbr_inscrit': nbr_inscrit,
        'nbr_inscrit_att': nbr_inscrit_att,
        'nbr_joueur': nbr_joueur,
        'nbr_joueur_att': nbr_joueur_att
        })


@login_required(login_url='../../accounts/login/')
def inscription_create(request, pk):
    joueur = request.user
    try:
        tourdejeu = TourDeJeu.objects.get(pk=pk)
    except TourDeJeu.DoesNotExist:
        return redirect('inscription')

    nbr_inscrit = tourdejeu.nbr_inscrit + 1
    TourDeJeu.objects.filter(pk=pk).update(nbr_inscrit=nbr_inscrit)

    joueur = ListJoueur(
        joueur_id=joueur,
        tourdejeu_id=tourdejeu,
        list_att=0,
    )
    joueur.save()
    
    return HttpResponse('')


@login_required(login_url='../../accounts/login/')
def inscription_att_create(request, pk):
    joueur = request.user
    try:
        tourdejeu = TourDeJeu.objects.get(pk=pk)
    except TourDeJeu.DoesNotExist:
        return redirect('inscription')
    
    nbr_inscrit_att = tourdejeu.nbr_inscrit_att + 1
    TourDeJeu.objects.filter(pk=pk).update(nbr_inscrit_att=nbr_inscrit_att)

    joueur = ListJoueur(
        joueur_id=joueur,
        tourdejeu_id=tourdejeu,
        list_att=1,
    )
    joueur.save()  

    return HttpResponse('')  


@login_required(login_url='../../accounts/login/')
def desinscription(request, pk):
    joueur = request.user
    try:
        tourdejeu = TourDeJeu.objects.get(pk=pk)
    except TourDeJeu.DoesNotExist:
        return redirect('inscription')

    nbr_inscrit = tourdejeu.nbr_inscrit - 1
    TourDeJeu.objects.filter(pk=pk).update(nbr_inscrit=nbr_inscrit)

    joueur_inscrit = ListJoueur.objects.filter(tourdejeu_id=pk).filter(joueur_id=joueur)

    if joueur_inscrit.exists():
        joueur_inscrit.delete()
    else:
        return redirect('inscription')

    return HttpResponse('')


@login_required(login_url='../../accounts/login/')
def desinscription_att(request, pk):
    joueur = request.user
    try:
        tourdejeu = TourDeJeu.objects.get(pk=pk)
    except TourDeJeu.DoesNotExist:
        return redirect('inscription')

    nbr_inscrit_att = tourdejeu.nbr_inscrit_att - 1
    TourDeJeu.objects.filter(pk=pk).update(nbr_inscrit_att=nbr_inscrit_att)

    joueur_inscrit_att = ListJoueur.objects.filter(tourdejeu_id=pk).filter(joueur_id=joueur)

    if joueur_inscrit_att.exists():
        joueur_inscrit_att.delete()
    else:
        return redirect('inscription')

    return HttpResponse('')


def calendrier(request):
    list_ligue = Ligue.objects.all()
    list_club = Club.objects.all()
    list_tourdejeu = TourDeJeu.objects.all().order_by('date', 'lieu_organisation__ligue__nom_ligue', 'lieu_organisation__short_name')
    saison = Saison.objects.filter(default=True).last()

    list_date = []
    start_date = saison.date_debut 
    end_date = saison.date_fin

    tournoi_date = start_date
    while tournoi_date <= end_date:
        list_date.append({
            'tournoi_date': tournoi_date,
        })

        tournoi_date = tournoi_date + timedelta(7)

    return render(request, 'calendrier.html', {
        'list_ligue': list_ligue,
        'list_club': list_club,
        'list_tourdejeu': list_tourdejeu,
        'list_date': list_date,
        })


def faq(request):
    return render(request, 'FAQ.html')