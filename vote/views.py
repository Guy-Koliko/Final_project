from django.shortcuts import render
import json
import requests
import jmespath
from .models import PollingStation, Region,Constituency,PoliticalParty

# Create your views here.

def index(request):
    res = requests.get('https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=1RNbt5aoaP97EKLlrFSO4_TIbNOtPT4CBQhrbNhopz-M&sheet=Sheet3')
    var = json.loads(res.text)

    #we get the chain from the API and load the json data
    # j = jmespath.search('chain[*].transaction',var)
    j = jmespath.search('Sheet3[*]',var)
    
    consts = Region.objects.all
    c_vote = PoliticalParty.objects.all
    context = {'data':consts,'c_vote':c_vote,'dat':j}
    return render(request,"vote/index.html",context)


def constituency(request):
     #this is the url to api
    res = requests.get('https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=1RNbt5aoaP97EKLlrFSO4_TIbNOtPT4CBQhrbNhopz-M&sheet=Sheet4')
    var = json.loads(res.text)

    #we get the chain from the API and load the json data
    # j = jmespath.search('chain[*].transaction',var)
    j = jmespath.search('Sheet4[*]',var)
    c_vote = PoliticalParty.objects.all
    p_station = Constituency.objects.all()
    context = {'data':c_vote,'poll':p_station,'dat':j}
    return render(request,"vote/vote_by_constituency.html",context)



def polling_station(request):
    
    #this is the url to api
    res = requests.get('https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=1RNbt5aoaP97EKLlrFSO4_TIbNOtPT4CBQhrbNhopz-M&sheet=Sheet1')
    var = json.loads(res.text)

    #we get the chain from the API and load the json data
    # j = jmespath.search('chain[*].transaction',var)
    j = jmespath.search('Sheet1[*]',var)
    
    
    # data from our database
    data = PollingStation.objects.all
    datas = PoliticalParty.objects.all

    print(j)

    context = {'data':data,'datas':datas,'dat':j}
    return render(request,"vote/vote_by_polling_station.html",context)

def add_list(m):
   return sum(int(m))

def vote_data_input(request):
    res = requests.get('http://127.0.0.1:9000/chain')
    var = json.loads(res.text)
    ps = PollingStation.objects.all
    

    j = jmespath.search('chain[*]',var)
  
  
    context = {'data':j,'ps':ps}
    return render(request,"vote/polling_station_data.html",context)


def political_party_stats(request):
    pp = PoliticalParty.objects.all 
    region = Region.objects.all
    context = {'data':pp,'reg':region}
    return render(request,"vote/political_parties_votes.html",context)