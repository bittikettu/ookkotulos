"""
Definition of views.
"""

import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import *
from .forms import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Etusivu',
            'year':2021,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Tekijät',
            'message':'Tekijät',
            'year':2021,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Sovelluksesta',
            'message':'Tietoa sovelluksesta',
            'year':2021,
        }
    )

def events(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    try:
        person = request.user #Person.objects.get(user=request.user)
        return render(
        request,
        'app/events.html',
        {
            'year':2021,
            'title':'Tapahtumat',
            'message':'Tulevat tapahtumat',
            'events': Event.objects.all().filter(date__gte=timezone.now()),
            'pastevents': Event.objects.all().filter(date__lte=timezone.now()),
            'eventsjoined': EventsJoined.objects.all().filter(person=request.user,join=True),
        }
    )
    except:
        print("not found")
        return render(
            request,
            'app/events.html',
            {
                'year':2021,
                'title':'Tapahtumat',
                'message':'Tulevat tapahtumat',
                'events':Event.objects.all(),
            }
        )

def cancelevent(request, pk):
    eventti = Event.objects.get(id=pk)
    person = request.user #Person.objects.get(user=request.user)
    joininfo = EventsJoined.objects.get(event=eventti,person=person)
    print(joininfo)
    joininfo.delete()
    #joininfo.cancelevent()
    #print(eventti)
    
    #print(person)
    #joininfo.save()
    return redirect('events')
    #return render(
    #    request,
    #    'app/events.html',
    #    {
    #        'title':'Tapahtumat',
    #        'message':'Tulevat tapahtumat',
    #        'events':Event.objects.all().filter(date__gte=timezone.now()),
    #        'pastevents':Event.objects.all().filter(date__lte=timezone.now()),
    #        'eventsjoined':EventsJoined.objects.all().filter(person=person),
    #        'year':2021,
    #    }
    #)

def joinevent(request, pk):
    eventti = Event.objects.get(id=pk)
    person = request.user #Person.objects.get(user=request.user)
    #derp = person.event_set.add(eventti)
    #print(derp)
    try:
        jointoevent = EventsJoined.objects.get(event=eventti,person=person)
    except:
        jointoevent = EventsJoined(person=person,event=eventti)
    jointoevent.jointoevent()
    #print(eventti)
    #print(jointoevent)
    #print(person)
    jointoevent.save()
    #LogEntry.objects.log_action(
    #            user_id=request.user.id,
     #           content_type_id=ContentType.objects.get_for_model(jointoevent).pk,
     #           object_id=jointoevent.id,
     #           object_repr=repr(jointoevent.title),
     #           action_flag=ADDITION if create else CHANGE)

    return redirect('events')
    #return render(
    #    request,
    #    'app/events.html',
    #    {
    #        'title':'Tapahtumat',
    #        'message':'Tulevat tapahtumat',
    #        'events':Event.objects.all().filter(date__gte=timezone.now()),
    #        'pastevents':Event.objects.all().filter(date__lte=timezone.now()),
    #        'eventsjoined': person.event_set.all() #EventsJoined.objects.all().filter(person=person),
    #    }
    #)

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            u = form.save(commit=False)
            #permission = Permission.objects.get(name='Can view poll')
            u.user_permissions.add(Permission.objects.get(name='Can add group'))
            return redirect("/login")
        else:
            return redirect("/register")
    else:
        form = RegisterForm()
    return render(
        response, 
        "app/register.html", 
        {
            'title':'Liity',
            'message':'Liity tapahtumailmoon',
            "form":form
        }
    )

def addevent(response):
    if response.method == "POST":
        form = AddeventForm(response.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = response.user
            event.save()
            form.save_m2m()

        return redirect("/events")
    else:
        form = AddeventForm()
    return render(
        response, 
        "app/addevent.html", 
        {
            'title':'Luo',
            'message':'Luo uusi tapahtuma ja kutsu kaverit mukaan.',
            "form":form
        }
    )