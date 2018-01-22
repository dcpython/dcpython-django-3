from django.shortcuts import render
from django.views.decorators.cache import cache_page
import requests
from django.utils import timezone
import os

# Create your views here.

MEETUP_API_URL = os.environ.get('MEETUP_API_URL', '')


@cache_page(300)
def home(request):
    context = {}
    if MEETUP_API_URL:
        url = '/'.join([MEETUP_API_URL, 'dcpython', 'events?sign=True'])
        response = requests.get(url)
    else:
        response = None
    events = []
    if response:
        for event in response.json():
            if not event['name'].startswith('[pending'):  # filter out pending
                ms = event['time']
                when = timezone.datetime.fromtimestamp(ms / 1000.0)
                event['when'] = when
                events.append(event)
        context['events'] = events[:3]  # Display first 3 events
    return render(request, 'home.html', context)


def aws(request):
    return render(request, 'aws.html', {})


def coc(request):
    return render(request, 'coc.html', {})


def donate(request):
    return render(request, 'donate.html', {})


def legal(request):
    return render(request, 'legal.html', {})


def team(request):
    return render(request, 'team.html', {})
