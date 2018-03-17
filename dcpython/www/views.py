from django.shortcuts import render
from django.views.decorators.cache import cache_page
import requests
from django.utils import timezone
import os

# Create your views here.

MEETUP_API_URL = os.environ.get('MEETUP_API_URL', 'https://api.meetup.com')
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


def about(request):
    return render(request, 'about.html', {})


def aws(request):
    return render(request, 'aws.html', {})


def coc(request):
    return render(request, 'coc.html', {})


def donate(request):
    return render(request, 'donate.html', {})


def jobs(request):
    return render(request, 'jobs.html', {})


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
    organizers = []
    boardmembers = []
    # dict_keys(['member_id', 'role', 'profile_url', 'created', 'bio',
    # 'photo', 'other_services', 'name', 'visited', 'photo_url', 'updated',
    # 'status', 'group'])
    if response:
        if response.status_code == 200:
            results = response.json()
            if 'results' in results:
                for organizer in results['results']:
                    # Fix Eddie's typo
                    if 'bio' in organizer and 'name' in organizer and 'role' in organizer:
                        if organizer['name'] == 'eddie welker':
                            organizer['bio'] = organizer['bio'].replace(
                                'DCPython metups', 'DC Python meetups')
                    # Add bios for Rami and Jonathan Street
                    if not 'bio' in organizer and 'name' in organizer:
                        if organizer['name'] == 'Rami':
                            organizer[
                                'bio'] = "Host of DC Python's 'Python Labs' held every Saturday."
                    if not 'bio' in organizer and 'name' in organizer:
                        if organizer['name'] == 'Jonathan Street':
                            organizer[
                                'bio'] = "Host of DC Python's 'Project Night' held the third Tuesday of the month, every month."
                    if (organizer['name'] == 'eddie welker'
                            or organizer['name'] == 'Jonathan Street'
                            or organizer['name'] == 'Rami'):
                        organizers.append(organizer)
                for boardmember in results['results']:
                    # Fix Eddie's typo
                    if (boardmember['name'] == 'Alex Clark'
                            or boardmember['name'] == 'Amy Clark'):
                        boardmembers.append(boardmember)
    context['organizers'] = organizers
    context['boardmembers'] = boardmembers
    return render(request, 'team.html', context)
