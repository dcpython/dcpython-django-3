from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def aws(request):
    return render(request, 'aws.html', {})


def team(request):
    return render(request, 'team.html', {})
