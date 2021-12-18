from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import json
import requests
import jmespath
from vote.models import Region,PoliticalParty,PollingStation,Constituency
from authenticate.models import UserRegistrations
from .models import VoteConfirm
# Create your views here.

def vote_recorde(request):
     res = requests.get('https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=1RNbt5aoaP97EKLlrFSO4_TIbNOtPT4CBQhrbNhopz-M&sheet=Sheet1')
     var = json.loads(res.text)
     
     j = jmespath.search('chain[*]',var)
     data = PoliticalParty.objects.all
     user = UserRegistrations.objects.all
     
     #user confirming vote
     if request.method == 'POST':
          userconfirm = request.POST['userconfirm']
          form = VoteConfirm(vote_confirm=userconfirm)
          form.save()
          
          
          

     context = {'dat':j,'data':data,'user':user}
     return render(request,'vote/voterecords/vote_data.html',context)
    
def vote_confirmation(request):
    
     return render(request,'vote/voterecords/vote_data_input.html')


