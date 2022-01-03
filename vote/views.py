from django.shortcuts import render
import json
import requests
import jmespath
from .models import PollingStation, Region,Constituency,PoliticalParty
from authenticate.models import EcOfficial
from django.contrib.auth.decorators import login_required 
from .blockchain import Block,BlockChain
from authenticate.views import login_user

from logging import exception
import json
import time

blockchian = BlockChain()
port = 8000
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:{}".format(port)


# Create your views here.
@login_required()
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

@login_required()
def constituency(request):
     #this is the url to api
    # res = requests.get('https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=1RNbt5aoaP97EKLlrFSO4_TIbNOtPT4CBQhrbNhopz-M&sheet=Sheet4')
    # var = json.loads(res.text)

    #we get the chain from the API and load the json data
    # j = jmespath.search('chain[*].transaction',var)
    # j = jmespath.search('Sheet4[*]',var)
    c_vote = PoliticalParty.objects.all
    p_station = Constituency.objects.all()
    context = {'data':c_vote,'poll':p_station,}
    return render(request,"vote/vote_by_constituency.html",context)

# ##############################################################################################
@login_required()
def polling_station(request):
    
    # Get the polling station name from the requests and continue
    region1 = request.GET.get('region',"")
    constituency1= request.GET.get('constituency',"")
    polling_station1= request.GET.get('ps',"")
    party1 = request.GET.get('party1',"")
    party2 = request.GET.get('party2',"")
    

    # mine what ever results have being  submitted b the ec 
    res = requests.get('http://127.0.0.1:5000/mine')

    #this is the url to api to request data about results 
    res = requests.get('http://127.0.0.1:5000/chain')
    var = json.loads(res.text)
    # get chain
    chain = var['chain']

    # # get transaction list 
    # print(chain[1]['transaction'])

    # # get vote list(iterate until we dont have chain[x]) starts here 
    # print(chain[1]['transaction'][0])

    # # get region
    # print(chain[1]['transaction'][0]['Greater Accra'])

    #  # get constituency
    # print(chain[1]['transaction'][0]['Greater Accra']['Amasaman-kese'])

    #    # get polling station
    # print(chain[1]['transaction'][0]['Greater Accra']['Amasaman-kese']['Amasaman '])

    #    # get party1 votes 
    # print(chain[1]['transaction'][0]['Greater Accra']['Amasaman-kese']['Amasaman ']['NDC '])

    #    # get party2 votes 
    # print(chain[1]['transaction'][0]['Greater Accra']['Amasaman-kese']['Amasaman ']['NPP '])

    #    # get party2 votes 
    # print(chain[1]['transaction'][0]['Greater Accra']['Amasaman-kese']['Amasaman ']['rejected_ballot'])

    
    
    #we get the chain from the API and load the json data
    j = jmespath.search('chain[*].transaction',var)
   
    # set polling station data to string and remove all spaces before  search
    ps = str(polling_station1.split()[0])

    # data from our database
    data = PollingStation.objects.filter(polling_station_name = ps)#we are retieving data for only one ps
    datas = PoliticalParty.objects.all()
    # for i in data:
    #     print(i.polling_station_name)

    # get the results 
    for i in j:
        if i:
            try:
                results = [ i[0][region1][constituency1][polling_station1][party1],i[0][region1][constituency1][polling_station1][party2]]
                rejected_ballot = i[0][region1][constituency1][polling_station1]['rejected_ballot']
                rb = [rejected_ballot]
            except:
                pass

    context = {'data':data,'datas':datas,'dat':results,'rb': rb }
    return render(request,"vote/vote_by_polling_station.html",context)

#####################################################################################
def add_list(m):
   return sum(int(m))



@login_required()
def vote_data_input(request):
    # res = requests.get('http://127.0.0.1:9000/chain')
    # var = json.loads(res.text)
    ps = PollingStation.objects.all
    

    # j = jmespath.search('chain[*]',var)
  
  
    context = {'data':'1','ps':ps}
    return render(request,"vote/polling_station_data.html",context)


################################
@login_required()
def political_party_stats(request):
    g = globals()
    General_results = []
    final_results = []
    final_results_value = []
    payload = []
    vsum = []

    party1sum = 0
    party2sum = 0 
    totalrejected = 0
    votedtotal = 0


    #################################
    # mine what ever results have being  submitted b the ec 
    res = requests.get('http://127.0.0.1:5000/mine')

    #this is the url to api to request data about results 
    res = requests.get('http://127.0.0.1:5000/chain')
    var = json.loads(res.text)
    # get chain
    chain = var['chain']

    #we get the chain from the API and load the json data
    data = jmespath.search('chain[*].transaction',var)

    ###################################
    pp = PoliticalParty.objects.all()
    pp1 = PoliticalParty.objects.all().order_by('name') #political parties
    region = Region.objects.all() #regions

    # Generate the individual party stats (party a,party b,rejected ballots )
    
    #  for every i in every region
    for i in region:
        # instantiate an empty list with the region name
        # g['region_{}'.format(i)] = []
        # print(region)

        # fetch the linked constituencies to that region
        constituencies = Constituency.objects.filter(region__region_name = str(i))
        # print(constituencies)

        # for  j in those constituencies
        for j in constituencies :
            
            # fetch the polling stations in each constituency
            ps = PollingStation.objects.filter( member_of__constituency_name = str(j))
            # print (ps)
            # for every poling station found in constituency
            for k in ps:
                # print(k)
                # for each partie in db 
                # for l in pp:
                    # print(str(l)+"_test")
                for u in data: 
                    if u:
                        # print(i,j,k,l)
                        try:
                            res = [str(i),u[0][str(i)][str(j)][str(k)][str(pp[0])],u[0][str(i)][str(j)][str(k)][str(pp[1])],u[0][str(i)][str(j)][str(k)]['rejected_ballot']]
                            General_results.append(res)
                        except:
                            pass

                
                            
                    # fetch the results 
                    # add the results for the parties to the list eg [ndc res,npp res]
                    # add rejected ballot to the list eg oti_results = [ndc res,npp res,rejected ballot res ]
            
            
        # finally add each results to general results and pass via context to the template 

    # General_results.append('region_{}'.format(i))     
    print(General_results)
    for results in General_results:
            if results[0] not in final_results:
                final_results.append(results[0])
                final_results_value.append([0,0,0,0])

            if results[0] in final_results:

                val1= results[1]
                val2= results[2]
                val3= results[3]
                

                index = final_results.index(results[0])

                final_results_value[index][0] += int(val1)
                final_results_value[index][1] += int(val2)
                final_results_value[index][2] += int(val3)
                final_results_value[index][3] =  final_results_value[index][3] + int(val1) + int(val2) + int(val3)

    print(final_results)
    print(final_results_value)


#  total party sum
    for i in final_results:
            index = final_results.index(i)
            party1sum += final_results_value[index][0]
            party2sum += final_results_value[index][1]
            totalrejected += final_results_value[index][2]
            votedtotal += final_results_value[index][3]

            votesum = {'ndcsum': party1sum ,'nppsum': party2sum,'totalrejected': totalrejected,'votedtotal': votedtotal,}
    vsum.append(votesum) 


#   individual regional results 
    for i in final_results:
        index = final_results.index(i)

        total = {'index': index,'region':i,'ndc': final_results_value[index][0],'npp': final_results_value[index][1],'rejected': final_results_value[index][2],'total': final_results_value[index][3],'percentage': (final_results_value[index][3]/votesum['votedtotal'])*100,}
        payload.append(total) 
    # print(payload)



#final voting result expressed in percentages
    # for i in final_results:
    npp_percentage = (votesum['nppsum']/ votesum['votedtotal']) * 100
    ndc_percentage = (votesum['ndcsum']/ votesum['votedtotal']) * 100
    rejected_percentage = (votesum['totalrejected']/ votesum['votedtotal']) * 100

    final_percentage = {"npp_percentage": npp_percentage,"ndc_percentage":ndc_percentage,"rejected_percentage":rejected_percentage,}
    vote_percentage_results = []
    vote_percentage_results.append(final_percentage)
    
    print(pp)
    context = {'data':pp,'reg':region,"final": payload , "sums" : vsum ,"percentage_res":vote_percentage_results,}
    return render(request,"vote/political_parties_votes.html",context)
#################################



@login_required()
def polling_station_stats(request):
    g = globals()
    General_results = []
    final_results = []
    final_results_value = []
    payload = []
    vsum = []

    party1sum = 0
    party2sum = 0 
    totalrejected = 0
    votedtotal = 0


    #################################
    # mine what ever results have being  submitted b the ec 
    res = requests.get('http://127.0.0.1:5000/mine')

    #this is the url to api to request data about results 
    res = requests.get('http://127.0.0.1:5000/chain')
    var = json.loads(res.text)
    # get chain
    chain = var['chain']

    #we get the chain from the API and load the json data
    data = jmespath.search('chain[*].transaction',var)

    ###################################
    pp = PoliticalParty.objects.all()
    pp1 = PoliticalParty.objects.all().order_by('name') #political parties
    region = Region.objects.all() #regions

    # Generate the individual party stats (party a,party b,rejected ballots )
    
    #  for every i in every region
    for i in region:
        # instantiate an empty list with the region name
        # g['region_{}'.format(i)] = []
        # print(region)

        # fetch the linked constituencies to that region
        constituencies = Constituency.objects.filter(region__region_name = str(i))
        # print(constituencies)

        # for  j in those constituencies
        for j in constituencies :
            
            # fetch the polling stations in each constituency
            ps = PollingStation.objects.filter( member_of__constituency_name = str(j))
            # print (ps)
            # for every poling station found in constituency
            for k in ps:
                # print(k)
                # for each partie in db 
                # for l in pp:
                    # print(str(l)+"_test")
                for u in data: 
                    if u:
                        # print(i,j,k,l)
                        try:
                            res = [str(k),u[0][str(i)][str(j)][str(k)][str(pp[0])],u[0][str(i)][str(j)][str(k)][str(pp[1])],u[0][str(i)][str(j)][str(k)]['rejected_ballot']]
                            General_results.append(res)
                        except:
                            pass

                
                            
                    # fetch the results 
                    # add the results for the parties to the list eg [ndc res,npp res]
                    # add rejected ballot to the list eg oti_results = [ndc res,npp res,rejected ballot res ]
            
            
        # finally add each results to general results and pass via context to the template 

    # General_results.append('region_{}'.format(i))     
    print(General_results)
    for results in General_results:
            if results[0] not in final_results:
                final_results.append(results[0])
                final_results_value.append([0,0,0,0])

            if results[0] in final_results:

                val1= results[1]
                val2= results[2]
                val3= results[3]
                

                index = final_results.index(results[0])

                final_results_value[index][0] += int(val1)
                final_results_value[index][1] += int(val2)
                final_results_value[index][2] += int(val3)
                final_results_value[index][3] =  final_results_value[index][3] + int(val1) + int(val2) + int(val3)

    print(final_results)
    print(final_results_value)


#  total party sum
    for i in final_results:
            index = final_results.index(i)
            party1sum += final_results_value[index][0]
            party2sum += final_results_value[index][1]
            totalrejected += final_results_value[index][2]
            votedtotal += final_results_value[index][3]

            votesum = {'ndcsum': party1sum ,'nppsum': party2sum,'totalrejected': totalrejected,'votedtotal': votedtotal,}
    vsum.append(votesum) 


#   individual regional results 
    for i in final_results:
        index = final_results.index(i)

        total = {'index': index,'region':i,'ndc': final_results_value[index][0],'npp': final_results_value[index][1],'rejected': final_results_value[index][2],'total': final_results_value[index][3],'percentage': (final_results_value[index][3]/votesum['votedtotal'])*100,}
        payload.append(total) 
    # print(payload)



#final voting result expressed in percentages
    # for i in final_results:
    npp_percentage = (votesum['nppsum']/ votesum['votedtotal']) * 100
    ndc_percentage = (votesum['ndcsum']/ votesum['votedtotal']) * 100
    rejected_percentage = (votesum['totalrejected']/ votesum['votedtotal']) * 100

    final_percentage = {"npp_percentage": npp_percentage,"ndc_percentage":ndc_percentage,"rejected_percentage":rejected_percentage,}
    vote_percentage_results = []
    vote_percentage_results.append(final_percentage)
    
    print(pp)
    context = {'data':pp,'reg':region,"final": payload , "sums" : vsum ,"percentage_res":vote_percentage_results,}
    return render(request,"vote/polling_station_stats.html",context)
#################################




@login_required()
def constituency_stats(request):
    g = globals()
    General_results = []
    final_results = []
    final_results_value = []
    payload = []
    vsum = []

    party1sum = 0
    party2sum = 0 
    totalrejected = 0
    votedtotal = 0


    #################################
    # mine what ever results have being  submitted b the ec 
    res = requests.get('http://127.0.0.1:5000/mine')

    #this is the url to api to request data about results 
    res = requests.get('http://127.0.0.1:5000/chain')
    var = json.loads(res.text)
    # get chain
    chain = var['chain']

    #we get the chain from the API and load the json data
    data = jmespath.search('chain[*].transaction',var)

    ###################################
    pp = PoliticalParty.objects.all()
    pp1 = PoliticalParty.objects.all().order_by('name') #political parties
    region = Region.objects.all() #regions

    # Generate the individual party stats (party a,party b,rejected ballots )
    
    #  for every i in every region
    for i in region:
        # instantiate an empty list with the region name
        # g['region_{}'.format(i)] = []
        # print(region)

        # fetch the linked constituencies to that region
        constituencies = Constituency.objects.filter(region__region_name = str(i))
        # print(constituencies)

        # for  j in those constituencies
        for j in constituencies :
            
            # fetch the polling stations in each constituency
            ps = PollingStation.objects.filter( member_of__constituency_name = str(j))
            # print (ps)
            # for every poling station found in constituency
            for k in ps:
                # print(k)
                # for each partie in db 
                # for l in pp:
                    # print(str(l)+"_test")
                for u in data: 
                    if u:
                        # print(i,j,k,l)
                        try:
                            res = [str(j),u[0][str(i)][str(j)][str(k)][str(pp[0])],u[0][str(i)][str(j)][str(k)][str(pp[1])],u[0][str(i)][str(j)][str(k)]['rejected_ballot']]
                            General_results.append(res)
                        except:
                            pass

                
                            
                    # fetch the results 
                    # add the results for the parties to the list eg [ndc res,npp res]
                    # add rejected ballot to the list eg oti_results = [ndc res,npp res,rejected ballot res ]
            
            
        # finally add each results to general results and pass via context to the template 

    # General_results.append('region_{}'.format(i))     
    print(General_results)
    for results in General_results:
            if results[0] not in final_results:
                final_results.append(results[0])
                final_results_value.append([0,0,0,0])

            if results[0] in final_results:

                val1= results[1]
                val2= results[2]
                val3= results[3]
                

                index = final_results.index(results[0])

                final_results_value[index][0] += int(val1)
                final_results_value[index][1] += int(val2)
                final_results_value[index][2] += int(val3)
                final_results_value[index][3] =  final_results_value[index][3] + int(val1) + int(val2) + int(val3)

    print(final_results)
    print(final_results_value)


#  total party sum
    for i in final_results:
            index = final_results.index(i)
            party1sum += final_results_value[index][0]
            party2sum += final_results_value[index][1]
            totalrejected += final_results_value[index][2]
            votedtotal += final_results_value[index][3]

            votesum = {'ndcsum': party1sum ,'nppsum': party2sum,'totalrejected': totalrejected,'votedtotal': votedtotal,}
    vsum.append(votesum) 


#   individual regional results 
    for i in final_results:
        index = final_results.index(i)

        total = {'index': index,'region':i,'ndc': final_results_value[index][0],'npp': final_results_value[index][1],'rejected': final_results_value[index][2],'total': final_results_value[index][3],'percentage': (final_results_value[index][3]/votesum['votedtotal'])*100,}
        payload.append(total) 
    # print(payload)



#final voting result expressed in percentages
    # for i in final_results:
    npp_percentage = (votesum['nppsum']/ votesum['votedtotal']) * 100
    ndc_percentage = (votesum['ndcsum']/ votesum['votedtotal']) * 100
    rejected_percentage = (votesum['totalrejected']/ votesum['votedtotal']) * 100

    final_percentage = {"npp_percentage": npp_percentage,"ndc_percentage":ndc_percentage,"rejected_percentage":rejected_percentage,}
    vote_percentage_results = []
    vote_percentage_results.append(final_percentage)
    
    print(pp)
    context = {'data':pp,'reg':region,"final": payload , "sums" : vsum ,"percentage_res":vote_percentage_results,}
    return render(request,"vote/constituency_stats.html",context)
#################################





# dashbpard for ecofficial 
@login_required
def ecdashboard(request):
    print(res.url)
    data = EcOfficial.objects.filter(user_code= username)

    # get parties ec is affiliated to 
    data1 = EcOfficial.objects.filter(user_code= username)
    parties = PoliticalParty.objects.filter(tag = data1.pollingstation)
    context = {'profiles':data ,"parties":parties}
    return render(request,"vote/ecdashboard.html",context)



