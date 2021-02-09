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
from django.contrib.auth.models import Group
import hashlib


def extrashit(request):
    addeventform = AddeventForm(user=request.user)
    joingroupform = JoinGroup()
    addgroupform = CreateGroup()
    return {
        "addeventform":addeventform,
        "joingroupform":joingroupform,
        "newroupform":addgroupform,
        }

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Etusivu',
            'year':2021,
            'users':Person.objects.all(),
            'events':Event.objects.all(),
            'events_joinable':Event.objects.all().filter(date__gte=timezone.now()),
            'joins': EventsJoined.objects.all(),
            'forms' : extrashit(request),
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
            'forms' : extrashit(request),
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
            'forms' : extrashit(request),
        }
    )

def addevent(response):
    if response.method == "POST":
        form = AddeventForm(response.POST,user=response.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = response.user
            event.save()
            form.save_m2m()
#next = request.POST.get('next', '/')
        return redirect(response.POST.get('next', '/'))
    else:
        form = AddeventForm(user=response.user)
    return render(
        response, 
        "app/addevent.html", 
        {
            'title':'Luo',
            'message':'Luo uusi tapahtuma ja kutsu kaverit mukaan.',
            "form":form
        }
    )


def events(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    

    try:
        person = request.user #Person.objects.get(user=request.user)
        #addeventform = AddeventForm(user=request.user)
        ##joingroupform = JoinGroup()
        #addgroupform = CreateGroup()
        return render(
        request,
        'app/events.html',
        {
            'year':2021,
            'title':'Tapahtumat modal',
            #"addeventform":addeventform,
            #"joingroupform":joingroupform,
            #"newroupform":addgroupform,
            'forms' : extrashit(request),
            'message':'Tulevat tapahtumat',
            #'events': Event.objects.all().filter(date__gte=timezone.now()),
            'events':Event.objects.all().filter(group__id__in=person.groups.all(),date__gte=timezone.now()).order_by('date'),
            #'pastevents': Event.objects.all().filter(date__lte=timezone.now()),
            #'eventsjoined': EventsJoined.objects.all().filter(join=True, event__date__gte=timezone.now()),
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
                #'events': Event.objects.all().filter(date__gte=timezone.now()),
                'events':Event.objects.all().filter(group__id__in=person.groups.all(),date__gte=timezone.now()).order_by('date'),
            }
        )

def cancelevent(request, pk):
    eventti = Event.objects.get(id=pk)
    person = request.user #Person.objects.get(user=request.user)
    joininfo = EventsJoined.objects.get(event=eventti,person=person)
    joininfo.delete()

    return redirect('events')


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
    #return redirect(request.POST.get('next', '/'))
    return redirect('events')


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            u = form.save(commit=False)
            #person = Person.objects.get(id=u.id)
            #print(person)
            u.save()
            permission = Permission.objects.get(name='Can add group')
            u.user_permissions.add(permission)
            u.save()

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



def creategroup(response):
    if response.method == "POST":
        form = CreateGroup(response.POST)
        if form.is_valid():
            g1 = Group.objects.create(name=form.cleaned_data['groupname'])
            g1.user_set.add(response.user)
        return redirect(response.POST.get('next', '/'))
        #return redirect("/events")
    else:
        form = CreateGroup()
    return render(
        response, 
        "app/creategroup.html", 
        {
            'title':'Tee uusi porukka',
            'message':'Luo uusi porukka kavereitasi varten',
            "form":form
        }
    )

#def md5_string(value):
#    return hashlib.md5(str(value).encode()).hexdigest()

def md5_string(value):
    return hashlib.md5(value.encode()).hexdigest()

def joingroup(response):
    if response.method == "POST": 
        form = JoinGroup(response.POST)
        if form.is_valid():
            for event in Event.objects.all():
                try:
                    if md5_string(event.group.name) == form.cleaned_data['groupname']:
                        try:
                            g1 = event.group
                            g1.user_set.add(response.user)
                        except:
                            print("User was on this group")
                    else:
                        print("Group not found")
                except:
                    pass
        return redirect(response.POST.get('next', '/')) #return redirect("/events")
    else:
        form = JoinGroup()
    return render(
        response, 
        "app/joingroup.html", 
        {
            'title':'Tee uusi porukka',
            'message':'Luo uusi porukka kavereitasi varten',
            "form":form
        }
    )

def user(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    person = request.user #Person.objects.get(user=request.user)
    return render(
    request,
    'app/user.html',
    {
        'year':2021,
        'title':'Käyttäjän tiedot',
        'message':'Käyttäjän tiedot',
        'groups': person,
        'events':Event.objects.filter(group__id__in=person.groups.all()).order_by('date'),
        'eventsjoined' : Event.objects.filter(members=person).order_by('date'),
        #'pastevents': Event.objects.all().filter(date__lte=timezone.now()),
        #'eventsjoined': EventsJoined.objects.all().filter(join=True, event__date__gte=timezone.now()),
    }
    )
