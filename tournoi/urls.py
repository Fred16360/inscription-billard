from django.urls import path

from tournoi import views


urlpatterns = [
    #path('inscription', views.inscription, name='inscription'),
    path('calendrier', views.calendrier, name='calendrier'),
    path('desinscription/<int:pk>', views.desinscription, name='desinscription'),
    path('desinscription_att/<int:pk>', views.desinscription_att, name='desinscription_att'),
   # path('create_season', views.create_season, name='create_season'),
    path('list_joueur/<int:pk>', views.list_joueur, name='list_joueur'),
    path('inscription_create/<int:pk>', views.inscription_create, name='inscription_create'),
    path('inscription_att_create/<int:pk>', views.inscription_att_create, name='inscription_att_create'),
    path('faq', views.faq, name='faq'),
]
