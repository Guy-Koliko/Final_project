from django.urls import path
from . import views

urlpatterns = [
    path('vote/', views.vote_recorde,name="vote_record"),
    path('record/',views.vote_confirmation,name="record")
]
