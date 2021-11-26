from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"vote/index.html")


def constituency(request):
    return render(request,"vote/vote_by_constituency.html")



def polling_station(request):
    return render(request,"vote/vote_by_polling_station.html")


def vote_data_input(request):
    return render(request,"vote/polling_station_data.html")


def political_party_stats(request):
    return render(request,"vote/political_parties_votes.html")