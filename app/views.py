"""
Definition of views.
"""

import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import *
from .forms import *

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
            'title':'Tapahtumat',
            'message':'Tulevat tapahtumat',
            'events':Event.objects.all(),
            'eventsjoined':EventsJoined.objects.all().filter(person=request.user),
        }
    )
    except:
        print("not found")
        return render(
            request,
            'app/events.html',
            {
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
    return render(
        request,
        'app/events.html',
        {
            'title':'Tapahtumat',
            'message':'Tulevat tapahtumat',
            'events':Event.objects.all(),
            'eventsjoined':EventsJoined.objects.all().filter(person=person),
        }
    )

def joinevent(request, pk):
    eventti = Event.objects.get(id=pk)
    person = request.user #Person.objects.get(user=request.user)
    try:
        jointoevent = EventsJoined.objects.get(event=eventti,person=person)
    except:
        jointoevent = EventsJoined(person=person,event=eventti)
    jointoevent.jointoevent()
    print(eventti)
    print(jointoevent)
    print(person)
    jointoevent.save()

    return render(
        request,
        'app/events.html',
        {
            'title':'Tapahtumat',
            'message':'Tulevat tapahtumat',
            'events':Event.objects.all(),
            'eventsjoined':EventsJoined.objects.all().filter(person=person),
        }
    )

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/login")
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