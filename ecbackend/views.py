from django.shortcuts import render
from authenticate.models import UserRegistrations,EcOfficial
from vote.models import Constituency,Region,PoliticalParty,PollingStation
'''
    This page is for the EC backend
    With this part the EC needs to check everything before sending
'''

def official_info(request):
    party = PoliticalParty.objects.all
    context = {"party":party}
    return render(request,"vote/ec_page/ec_backend_info.html",context)

def party_infor(request):
    user = UserRegistrations.objects.all
    context = {"user":user}
    return render(request,"vote/ec_page/party_info.html",context)

def ec_official(request):
    user = EcOfficial.objects.all
    context = {"ec":user}
    return render(request,"vote/ec_page/ec_official_page.html",context)


def final_confirmation(request):
    return render(request,"vote/ec_page/final_confirmation.html")