"""
Definition of views.
"""

import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import *
from .forms import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE,DELETION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
import hashlib
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.urls import reverse
from .utils import logshit


def extrashit(request):
    if(request.user):
        addeventform = CreateEventForm(user = request.user)
        joingroupform = JoinGroup()
        addgroupform = CreateGroup()
        return {
            "addeventform":addeventform,
            "joingroupform":joingroupform,
            "newroupform":addgroupform,
            'versio': "1.0",
            }
    else:
        return {}


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
            'events_joinable':Event.objects.all().filter(date__gte = timezone.now()),
            'joins': EventsJoined.objects.all(),
            'forms': extrashit(request),
            'news' : News.objects.all().order_by("id").reverse()
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
            'forms': extrashit(request),
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
            'forms': extrashit(request),
        }
    )



def eventremove(response, pk):
    if response.user.is_authenticated:
        event = Event.objects.get(pk = pk)
        logshit(response, event, "message",DELETION)
        event.delete()
    return redirect('events')


def eventsettings(response, pk):
    event = Event.objects.get(pk = pk)
    print(event)
    print(pk)
    if response.method == "POST":
        form = CreateEventForm(response.POST, user = response.user)
        if form.is_valid():
            #print(form.fields.items())
            #print(form.changed_data)
            print(form.cleaned_data['date'])
            print(form['date'])
            event.creator = response.user
            event.name = form.cleaned_data['name']
            event.type = form.cleaned_data['type']
            event.max = form.cleaned_data['max']
            event.date = form.cleaned_data['date']
            event.description = form.cleaned_data['description']
            event.save()
            logshit(response, event, "message",CHANGE)
            return redirect('events')
            # eventselected = form.save(commit = False)
            # eventselected.creator = response.user
            # eventselected.save()
            # form.save_m2m()
#             return render(
#                 response,
#                 "app/eventsettings.html",
#                 {
#                     'title':'Muokkaa',
#                     'message':'Muokkaa tapahtumaa',
#                     "form": form
#                 }
#             )
    else:
        form = CreateEventForm(user = response.user, instance = event)
    return render(
        response,
        "app/eventsettings.html",
        {
            'title':'Muokkaa',
            'message':'Muokkaa tapahtumaa',
            "form": form,
            'forms': extrashit(response),
            'changes': LogEntry.objects.all().filter(content_type=ContentType.objects.get_for_model(Event),object_id=pk),
            "id" : pk,
        }
    )


def events(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    try:
        person = request.user  # Person.objects.get(user=request.user)
        # addeventform = AddeventForm(user=request.user)
        # #joingroupform = JoinGroup()
        # addgroupform = CreateGroup()
        return render(
        request,
        'app/events.html',
        {
            'year':2021,
            'title':'Tapahtumat',
            # "addeventform":addeventform,
            # "joingroupform":joingroupform,
            # "newroupform":addgroupform,
            'forms': extrashit(request),
            'message':'Tulevat tapahtumat',
            # 'events': Event.objects.all().filter(date__gte=timezone.now()),
            'events':Event.objects.all().filter(group__id__in = person.groups.all(), date__gte = timezone.now()).order_by('date'),
            # 'pastevents': Event.objects.all().filter(date__lte=timezone.now()),
            # 'eventsjoined': EventsJoined.objects.all().filter(join=True, event__date__gte=timezone.now()),
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
                # 'events': Event.objects.all().filter(date__gte=timezone.now()),
                'events':Event.objects.all().filter(group__id__in = person.groups.all(), date__gte = timezone.now()).order_by('date'),
            }
        )


def cancelevent(request, pk):
    eventti = Event.objects.get(id = pk)


    person = request.user  # Person.objects.get(user=request.user)
    try:
        joininfo = EventsJoined.objects.get(event = eventti, person = person)
        joininfo.delete()
    except:
        pass

    return redirect('events')


def joinevent(request, pk):
    eventti = Event.objects.get(id = pk)
    person = request.user  # Person.objects.get(user=request.user)
    # derp = person.event_set.add(eventti)
    # print(derp)
    try:
        jointoevent = EventsJoined.objects.get(event = eventti, person = person)
    except:
        jointoevent = EventsJoined(person = person, event = eventti)
    jointoevent.jointoevent()
    # print(eventti)
    # print(jointoevent)
    # print(person)
    logshit(request, jointoevent, "message",ADDITION)
    jointoevent.save()
    # LogEntry.objects.log_action(
    #            user_id=request.user.id,
    #           content_type_id=ContentType.objects.get_for_model(jointoevent).pk,
    #           object_id=jointoevent.id,
    #           object_repr=repr(jointoevent.title),
    #           action_flag=ADDITION if create else CHANGE)
    # return redirect(request.POST.get('next', '/'))
    return redirect('events')


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            u = form.save(commit = False)
            # person = Person.objects.get(id=u.id)
            # print(person)
            u.save()
            permission = Permission.objects.get(name = 'Can add group')
            u.user_permissions.add(permission)
            u.save()

            return redirect("/login")
        else:
            render(
                response,
                "app/register.html",
                {
                    'title':'Liity',
                    'message':'Liity tapahtumailmoon',
                    "form":form
                }
            )
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
            g1 = Group.objects.create(name = form.cleaned_data['groupname'])
            g1.user_set.add(response.user)
            logshit(response, g1, "message",ADDITION)
        return redirect(response.POST.get('next', '/'))
        # return redirect("/events")
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


def md5_string(value):
    return hashlib.md5(value.encode()).hexdigest()


def joingroup(response):
    if response.method == "POST":

        form = JoinGroup(response.POST)
        if form.is_valid():
            for group in Group.objects.all():

                try:
                    # print(md5_string(event.group.name))

                    if md5_string(group.name) == form.cleaned_data['groupname']:
                        try:
                            g1 = group
                            g1.user_set.add(response.user)
                            logshit(response, g1, "message",ADDITION)
                        except:
                            print("User was on this group")
                    else:
                        print("Group not found")
                except:
                    pass
        return redirect(response.POST.get('next', '/'))  # return redirect("/events")
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


class CreateEventView(CreateView):
    model = Event
    form_class = CreateEventForm
        
    #def dispatch(self, *args, **kwargs):
    #    return super(CreateEventView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateEventView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        form.save_m2m()
        logshit(self.request, self.object, "message",ADDITION)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("events") #return reverse('system-detail', kwargs={'pk': self.object.pk})


class EventList(ListView):
    model = Event

    def get_queryset(self):
        return Event.objects.filter(group__id__in=self.request.user.groups.all()).order_by('date')

    def get_context_data(self, **kwargs):
        print(self.request.user)
        context = super().get_context_data(**kwargs)
        context['forms'] = extrashit(self.request)
        context['year'] = 2021
        context['title'] = 'Käyttäjän tiedot'
        context['message'] = 'Käyttäjän tiedot'
        context['changes'] = LogEntry.objects.all().filter(user=self.request.user)
        print(LogEntry.objects.all().filter(user=self.request.user))
        
        return context
