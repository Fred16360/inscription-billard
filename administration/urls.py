from django.urls import path, register_converter
from datetime import datetime
from . import views

from administration import views
from .views import SaisonList, SaisonCreate, SaisonUpdate, ListJoueurPDF


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy-mm-dd')


urlpatterns = [
    path('admin_index/<int:pg_prec>/<int:pg_suiv>', views.admin_index, name='admin_index'),
    path('admin_index/pdf/<int:pg_prec>/<int:pg_suiv>', views.admin_index_pdf, name='admin_index_pdf'),
    path('admin_update_tourdejeu/<int:pk>', views.TourdejeuUpdate, name='admin_update_tourdejeu'),
    path('admin_saison_list', SaisonList.as_view(), name='admin_saison_list'),
    path('admin_saison_create', views.SaisonCreate, name='admin_saison_create'),
    path('admin_saison_update/<int:pk>', views.SaisonUpdate, name='admin_saison_update'),

    path('admin_list_joueur/<int:pk>', ListJoueurPDF.as_view(), name='admin_listjoueur_pdf')
]
