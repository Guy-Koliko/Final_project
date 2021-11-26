from django.shortcuts import render

# Create your views here.

def vote_recorde(request):
    return render(request,'vote/voterecords/vote_data_input.html')


def vote_confirmation(request):
    return render(request,'vote/voterecords/vote_data.html')


