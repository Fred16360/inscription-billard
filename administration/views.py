from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta, time
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from tournoi.models import Ligue, Club, ModeJeux, TourDeJeu, ListJoueur
from administration.models import Saison
from .forms import TourdejeuForm, SaisonForm


# Create your views here.

@login_required(login_url='../../../../accounts/login/')
def admin_index(request, pg_prec, pg_suiv):
    list_ligue = Ligue.objects.all()
    list_club = Club.objects.all()
    list_tourdejeu = TourDeJeu.objects.all().order_by('date', 'lieu_organisation__ligue__nom_ligue', 'lieu_organisation__short_name')
    saison = Saison.objects.filter(default=True).last()

    list_date = []
    start_date = saison.date_debut + timedelta(pg_prec * 42)
    end_date = saison.date_debut + timedelta(pg_suiv * 42)

    tournoi_date = start_date
    while tournoi_date <= end_date:
        list_date.append({
            'tournoi_date': tournoi_date,
        })

        tournoi_date = tournoi_date + timedelta(7)

    return render(request, 'admin_index.html', {
        'list_ligue': list_ligue,
        'list_club': list_club,
        'list_tourdejeu': list_tourdejeu,
        'list_date': list_date,
        'pg_prec': pg_prec,
        'pg_suiv': pg_suiv,
        })


@login_required(login_url='../../../../accounts/login/')
def admin_index_pdf(request, pg_prec, pg_suiv):
    list_ligue = Ligue.objects.all()
    list_club = Club.objects.all()
    list_tourdejeu = TourDeJeu.objects.all().order_by('date', 'lieu_organisation__ligue__nom_ligue', 'lieu_organisation__short_name')
    saison = Saison.objects.filter(default=True).last()

    list_date = []
    start_date = saison.date_debut + timedelta(pg_prec * 42)
    end_date = saison.date_debut + timedelta(pg_suiv * 42)

    tournoi_date = start_date
    while tournoi_date <= end_date:
        list_date.append({
            'tournoi_date': tournoi_date,
        })

        tournoi_date = tournoi_date + timedelta(7)

    return render(request, 'admin_index_pdf.html', {
        'list_ligue': list_ligue,
        'list_club': list_club,
        'list_tourdejeu': list_tourdejeu,
        'list_date': list_date,
        'pg_prec': pg_prec,
        'pg_suiv': pg_suiv,
        })


@login_required(login_url='../../accounts/login/')
def TourdejeuUpdate(request, pk):
    
    try:
        tourdejeu = TourDeJeu.objects.get(pk=pk)
    except TourDeJeu.DoesNotExist:
        return redirect('admin_index')
        
    form = TourdejeuForm(request.POST or None, instance=tourdejeu)
    if form.is_valid():
        form.save()

       # tourdejeu.date.replace(hour=18, minute=00, second=00)
       # tourdejeu.save()

       # return redirect('admin_index')

    return render(request, 'admin_update_tourdejeu.html', {'form':form})


class SaisonList(LoginRequiredMixin, ListView):
    login_url = 'accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Saison

    template_name = 'admin_saison_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saison_list'] = Saison.objects.all().order_by('nom_saison')
        return context


@login_required(login_url='../../accounts/login/')
def SaisonCreate(request):
    form = SaisonForm()

    if request.method == "POST":
        form = SaisonForm(request.POST or None)
        if form.is_valid():
            form.save()
        
            list_club = Club.objects.all()
            saison = Saison.objects.filter(default=True).last()
            start_date = saison.date_debut
            end_date = saison.date_fin

            tournoi_date = start_date
            while tournoi_date <= end_date:
                list_tournoi = TourDeJeu.objects.filter(date=tournoi_date)
                if not list_tournoi.exists():
                    for club in list_club:
                        b = TourDeJeu(
                            tour_nbr = 0,
                            lieu_organisation = Club.objects.get(id=club.id),
                            mode_jeu = ModeJeux.objects.get(id=1),
                            nbr_maxi_joueur = 8,
                            date = tournoi_date
                        )
                        b.save()
                tournoi_date = tournoi_date + timedelta(7)
            return redirect('admin_saison_list')
        
    return render(request, "admin_saison_form.html", {'form':form, 'create': 1})        


@login_required(login_url='../../accounts/login/')
def SaisonUpdate(request, pk):
    try:
        saison = Saison.objects.get(id=pk)
    except Saison.DoesNotExist:
        return redirect('admin_saison_list')

    form = SaisonForm(request.POST or None, instance=saison)
    if form.is_valid():
        form.save()
        return redirect('admin_saison_list')
    
    return render(request, 'admin_saison_form.html', {'form':form, 'create': 0})



@login_required(login_url='../../accounts/login/')
def create_season(request):
    list_club = Club.objects.all()
    saison = Saison.objects.all().last()

    start_date = saison.date_debut
    end_date = saison.date_fin
    '''
    start_date = datetime.strptime('2021-12-05', '%Y-%m-%d')
    end_date = datetime.strptime('2022-01-16', '%Y-%m-%d')
    '''
    tournoi_date = start_date
    while tournoi_date <= end_date:
        list_tournoi = TourDeJeu.objects.filter(date=tournoi_date)
        if not list_tournoi.exists():
            for club in list_club:
                b = TourDeJeu(
                    tour_nbr = 0,
                    lieu_organisation = Club.objects.get(id=club.id),
                    mode_jeu = ModeJeux.objects.get(id=1),
                    nbr_maxi_joueur = 8,
                    date = tournoi_date
                )
                b.save()
        tournoi_date = tournoi_date + timedelta(7)

    return render(request, "index.html", {'list_tournoi':list_tournoi})


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


class ListJoueurPDF(LoginRequiredMixin, View):
    login_url = '../../accounts/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk, *args, **kwargs):
        modejeu = TourDeJeu.objects.get(pk=pk)
        if modejeu.mode_jeu.id == 1:
            return redirect('admin_index_pdf', pg_prec=0, pg_suiv=1)
        
        tourdejeu = TourDeJeu.objects.filter(mode_jeu=modejeu.mode_jeu).filter(tour_nbr=modejeu.tour_nbr)
        listjoueur = ListJoueur.objects.all()
        '''
        refmatch = RefMatch.objects.get(pk=pk)
        listpoint = Points.objects.filter(match=refmatch)
        '''
        pdf = render_to_pdf('admin_listjoueur_pdf.html', {'tourdejeu': tourdejeu, 'listjoueur':listjoueur, })
        return HttpResponse(pdf, content_type='application/pdf')









'''
        tdj = TourDeJeu(
            tour_nbr=form.cleaned_data["tour_nbr"],
            lieu_organisation=form.cleaned_data[""],
            mode_jeu=form.cleaned_data["mode_jeu"],
            nbr_maxi_joueur=form.cleaned_data["nbr_maxi_joueur"],
            nbr_inscrit=form.cleaned_data["nbr_inscrit"],
            nbr_inscrit_att=form.cleaned_data["nbr_inscrit_att"],
            date=date_fer
        )
        tdj.save()


'''