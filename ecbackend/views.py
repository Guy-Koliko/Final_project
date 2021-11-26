from django.shortcuts import render

# Create your views here.

def official_info(request):
    return render(request,"vote/ec_page/ec_backend_info.html")

def party_infor(request):
    return render(request,"vote/ec_page/party_info.html")


def final_confirmation(request):
    return render(request,"vote/ec_page/final_confirmation.html")