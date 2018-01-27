from django.shortcuts import render
from django.views.decorators.cache import cache_page
import requests
from django.utils import timezone
import os

# Create your views here.

MEETUP_API_URL = os.environ.get('MEETUP_API_URL', '')
MEETUP_API_KEY = os.environ.get('MEETUP_API_KEY', '')


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
    context = {}
    # https://api.meetup.com/2/profiles?&sign=true&photo-host=public
    # &role=leads&group_urlname=dcpython&page=20
    if MEETUP_API_URL:
        url = ''.join([
            MEETUP_API_URL, '/2/profiles', '?sign=True', '&role=leads',
            '&group_urlname=dcpython',
            '&key=%s' % MEETUP_API_KEY
        ])
        response = requests.get(url)
    else:
        response = None
    leads = []
    # dict_keys(['member_id', 'role', 'profile_url', 'created', 'bio',
    # 'photo', 'other_services', 'name', 'visited', 'photo_url', 'updated',
    # 'status', 'group'])
    if response.status_code == 200:
        results = response.json()
        if 'results' in results:
            for lead in results['results']:
                leads.append(lead)
    context['leads'] = leads
    return render(request, 'team.html', context)
