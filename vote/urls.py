from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('constituency/',views.constituency,name="const"),
    path('polling_station/',views.polling_station,name="poll"),
    path('vote_data_input/',views.vote_data_input,name='datas'),
    path('politica_party_stats/',views.political_party_stats,name='party'),
    path('dashboard/',views.ecdashboard,name='ecdashboard'),
    path('polling_station_stats/',views.polling_station_stats,name='pstats'),
    # constituency_stats
    path('constituency_stats/',views.constituency_stats,name='cstats')
]
