from django.shortcuts import render
from django.views.decorators.cache import cache_page
from json.decoder import JSONDecodeError
import requests

# Create your views here.

@cache_page(300)
def home(request):
    context = {}
    try:
        events = get_events()
        context['events'] = events
    except JSONDecodeError:
        pass
    return render(request, 'home.html', context)


def aws(request):
    return render(request, 'aws.html', {})

def coc(request):
    return render(request, 'coc.html', {})

def team(request):
    return render(request, 'team.html', {})

def events(request):
    url = '/'.join([settings.MEETUP_API_URL, 'dcpython', 'events?sign=True'])
    response = requests.get(url)
    events = []
    for event in response.json():
        if not event['name'].startswith('[pending'):  # filter out pending
            ms = event['time']
            when = timezone.datetime.fromtimestamp(ms/1000.0)
            event['when'] = when
            events.append(event)
    return events[:3]  # Display first 3 events
