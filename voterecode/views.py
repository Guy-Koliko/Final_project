from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import json
import requests
import jmespath
from vote.models import Region,PoliticalParty,PollingStation,Constituency
from authenticate.models import UserRegistrations
from .models import VoteConfirm
from django.contrib import messages
# Create your views here.

def vote_recorde(request):
     results = []
     rb = []

     #user confirming vote
     if request.method == 'POST':
          user = request.GET.get('user',"")
          userconfirm = request.POST['userconfirm']

          # check if that is the code for the user 
          if str(user) == str(userconfirm):
               # save the vote to db
               form = VoteConfirm(vote_confirm=userconfirm)
               form.save()
               messages.success(request,("Vote results confirmed"))
               # return redirect('')

          else:
               messages.success(request,("Error confirming vote data,please confirm identity by logging in again ."))
               return redirect('login')

          

    

     # Get the polling station name from the requests and continue
     region1 = request.GET.get('region',"")
     constituency1= request.GET.get('constituency',"")
     polling_station1= request.GET.get('ps',"")
     party1 = request.GET.get('party1',"NDC ")
     party2 = request.GET.get('party2',"NPP ")
     user = request.GET.get('user',"")

     # Add trailing space t0 fit condition
     polling_station1 = str(polling_station1) + " " 

     print(user)
     # print(region1,constituency1+"_t",polling_station1+"_t")
     
     #this is the url to api to request data about results 
     res = requests.get('http://127.0.0.1:5000/chain')
     var = json.loads(res.text)
     # get chain
     chain = var['chain']

     #we get the chain from the API and load the json data
     j = jmespath.search('chain[*].transaction',var)
     
     # set polling station data to string and remove all spaces before  search
     ps = str(polling_station1.split()[0])

     # data from our database
     data = PollingStation.objects.filter(polling_station_name = ps)#we are retieving data for only one ps
     datas = PoliticalParty.objects.all()
     
     for i in j:
          if i:
               print('check')
               try:
                    results = [ i[0][region1][constituency1][polling_station1][party1],i[0][region1][constituency1][polling_station1][party2]]
                    rejected_ballot = i[0][region1][constituency1][polling_station1]['rejected_ballot']
                    rb = [rejected_ballot]  
               except:
                    pass
     context = {'data':data,'datas':datas,'dat':results,'rb': rb }  
     return render(request,'vote/voterecords/vote_data.html',context)
          
     
     
     
 






def vote_confirmation(request):
    
     return render(request,'vote/voterecords/vote_data_input.html')


