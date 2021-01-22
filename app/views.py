"""
Definition of views.
"""

import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import *

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
    return render(
        request,
        'app/events.html',
        {
            'title':'Tapahtumat',
            'message':'Tulevat tapahtumat',
            'events':Event.objects.all(),
        }
    )