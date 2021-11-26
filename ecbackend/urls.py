from django.urls import path
from . import views

urlpatterns = [
    path('official/',views.official_info,name="official"),
    path('party_info/',views.party_infor,name="party_info"),
    path('final/',views.final_confirmation,name="final"),
]
