from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.

def login_user (request):
    if request.method == "POST":
        username = request.POST['username']
        passcode = request.POST['passcode']
        user = authenticate(request, username=username, password=passcode)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in!"))
            
            if user.username =="robin":
                return redirect('official')
            return redirect('vote_record')
        else:
            messages.success(request,("Error loging in, please try again."))
            return redirect('login')
    else:
        return render(request,'vote/authenticate/login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request,("Error loging in, please try again."))
    return redirect('login')
    


def register(request):
    return render(request,'vote/authenticate/register.html')