from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import EcOfficial,UserRegistrations
from vote.models import Region,PoliticalParty,PollingStation,Constituency
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login_user (request):
    if request.method == "POST":
        username = request.POST['username']
        passcode = request.POST['passcode']
        user = authenticate(request, username=username, password=passcode)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in!"))

            # redirect to dashboard for ec officer 
            if (user.username.split("-")[0]) == "EC":
              
               # Get ec profile
                data = EcOfficial.objects.filter(user_code= username)
                

                # get parties  ec is affiliated to 
                data1= EcOfficial.objects.get(user_code= username)
                parties = PoliticalParty.objects.all()
                context = {'profiles':data ,"parties":parties}


                return render(request,'vote/ecdashboard.html' ,context)
            
             # redirect to dashboard for party agent  
            if (user.username.split("-")[0]) == "PA":
                
                # codes
                # eg : PA-5-NE-CM-ASM-NPP
                r = (user.username.split("-")[2]) #r
                c = (user.username.split("-")[3]) #c
                p = (user.username.split("-")[4]) #p
            
                # get objects from db
                region_code = Region.objects.get(region_code = r )
                constituency_code = Constituency.objects.get(constituency_code= c)
                author_code = PollingStation.objects.get(pollingstation_code = p)

                # get names of codes 
                region = region_code.region_name
                constituency = constituency_code.constituency_name
                author = author_code.polling_station_name


                # pass the needed info to the url
                url = ('http://127.0.0.1:8000/vote/?region={}&constituency={}&ps={}&user={}').format(region,constituency,author,user.username) 
                
                # redirect to the route
                return redirect(url)

        else:
            messages.success(request,("Error loging in, please try again."))
            return redirect('login')
    else:
        return render(request,'vote/authenticate/login.html')
  
def logout_user(request):
    logout(request)
    messages.success(request,("Error loging in, please try again."))
    return redirect('login')
    

##################################################################################################
def register(request):
    # a lot of clean up to do here 
    if request.method == "POST":
        # right thing to do , form field validations  ,time not available 

        
        party_agent_sign_up = request.POST.get("inlineRadioOptions",'')
        ec_official_sign_up = request.POST.get("inlineRadioOptions",'')

        firstname = request.POST.get("firstname",'')
        lastname = request.POST.get("lastname",'')
        phone_number = request.POST.get("phonenumber",'')

        constituency = request.POST.get("consti",'')
        region = request.POST.get("region",'')
        polling_station = request.POST.get("pollingstation",'')
        party =  request.POST.get("party",'')



# ecofficial registration
        if int(ec_official_sign_up) == int(2):
            # if essential values are missing alert invalid input 
            if firstname and lastname and  phone_number  is None:
                messages.error(request,("first name ,lastname and phone number recquired"))

            if constituency =="Constituency" and polling_station == "Polling Station"   and region == "Region":
                messages.error(request,("Constituency,polling station and region recquired"))
                return redirect('register')


            # check if ec for that polling station exists
            condition = EcOfficial.objects.filter(pollingstation__id = polling_station,consituenc__id = constituency,region__id = region)
            print(condition)
            if condition:
                # dont sign up ec official for that polling station 
                messages.error(request,("ECOfficial is already Registered"))
                return redirect('register')
            
            # sign up ec offical for polling station
            else:
            
                # usercode = "EC-1-GAR-A-MN"

                # register ecofficial  
                ecobject = EcOfficial.objects.create(
                first_name = firstname  ,
                last_name = lastname ,
                region = Region.objects.get(id = region),
                consituenc = Constituency.objects.get(id =constituency) ,
                phone_number =  phone_number ,
                pollingstation = PollingStation.objects.get(id = polling_station)
                )

                # generate code
                # ############# 

                ec_code = "EC"

                # get registerd ec id
                ec_object = EcOfficial.objects.get(phone_number =  phone_number)
                ec_id = ec_object.pk

                # Get region code 
                r_object = Region.objects.get(id = region)
                r_code = r_object.region_code

                # get constituency code 
                c_object = Constituency.objects.get(id = constituency)
                c_code = c_object.constituency_code

                # get polling station code 
                p_object = PollingStation.objects.get(id = polling_station)
                p_code = p_object.pollingstation_code

                usercode = str(ec_code) + "-"+ str(ec_id) + "-"+ str(r_code) + "-"+ str(c_code) + "-"+ str(p_code)
                usercode = str(usercode)
                
                
                # uspdate usercode in model
                EcOfficial.objects.filter(phone_number =  phone_number).update(user_code = usercode)
               

                # map account to django default user auth 
                user = User.objects.create_user(username = usercode, password = phone_number)

                # success message 
                messages.success(request,("congrats you have being registered as ECofficial ,Please use {} and {} as your credentials to login").format(usercode,phone_number))
                return redirect('login')

# party agent registration
        if int(party_agent_sign_up) == int(1):
            # check if party agent for that polling station exists
            condition = UserRegistrations.objects.filter(party__id = party,pollingstation__id = polling_station,consituenc__id = constituency,region__id = region)
            if condition:
                # dont sign up ec official for that polling station 
                messages.success(request,("party agent for data already exists"))
                return redirect('register')
            
            # sign up party agent for polling station
            else:
           
                # usercode =  "PA-1-GAR-A-AM-NPP"

                # register party agent 
                UserRegistrations.objects.create(
                first_name = firstname  ,
                last_name = lastname ,
                region = Region.objects.get(id = region),
                consituenc = Constituency.objects.get(id = constituency),
                party = PoliticalParty.objects.get(id = party),
                phone_number =  phone_number ,
                pollingstation = PollingStation.objects.get(id = polling_station),
                # personal = 2
                )

                #     # generate code
                # ############# 

                pa_code = "PA"

                # get registerd ec id
                pa_object = UserRegistrations.objects.get(phone_number =  phone_number)
                pa_id = pa_object.pk

                # Get region code 
                r_object = Region.objects.get(id = region)
                r_code = r_object.region_code

                # get constituency code 
                c_object = Constituency.objects.get(id = constituency)
                c_code = c_object.constituency_code

                # get polling station code 
                p_object = PollingStation.objects.get(id  = polling_station)
                p_code = p_object.pollingstation_code

                # get party name 
                party_object = PoliticalParty.objects.get(id = party)
                party_name = party_object.name

                usercode = str(pa_code) + "-"+ str(pa_id) + "-"+ str(r_code) + "-"+ str(c_code) + "-"+ str(p_code) + "-"+ str(party_name)
                usercode = str(usercode)

                # uspdate usercode in model
                UserRegistrations.objects.filter(phone_number =  phone_number).update(user_code = usercode)

                 # map account to django default user auth 
                user = User.objects.create_user(username = usercode, password = phone_number)

                messages.success(request,("congrats you have being registered as an agent,use {} and {} as your credentials to login").format(usercode,phone_number))
                return redirect('login')

#####################################################################################################
    # get data
    regions =Region.objects.all()
    constituencies = Constituency.objects.all()
    pollingstations = PollingStation.objects.all()
    parties = PoliticalParty.objects.all()

    # Pass to page 
    context = {"regions": regions,"constituencies":constituencies,"pollingstations":pollingstations,"parties":parties,}
    return render(request,'vote/authenticate/register.html',context)


# end point to load the following data in flask view to populate the page 
# def Ecprofiledata(request):
#     EcOfficial.objects.get(



#     return redirect('login')

     