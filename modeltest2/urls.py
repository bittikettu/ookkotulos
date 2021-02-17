"""
Definition of urls for modeltest2.
"""

from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
import django.contrib.auth.forms
from app.views import EventList


urlpatterns = [
    #common shiz
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    
    # group management
    path("group/create/", views.creategroup, name="creategroup"),
    path("group/join/", views.joingroup, name="joingroup"),
    
    # event management
    path('event/all/', views.events, name='events'),
    path("event/add/", views.CreateEventView.as_view(), name="addevent"),
    path('event/modify/<str:pk>/', views.eventsettings, name='eventsettings'),
    path('event/remove/<str:pk>/', views.eventremove, name='eventremove'),
    path('event/cancel/<str:pk>/', views.cancelevent, name='cancelevent'),
    path('event/join/<str:pk>/', views.joinevent, name='joinevent'),
    
    # user management
    path("register/", views.register, name="register"),
    path('user/', EventList.as_view(), name="user"),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Kirjaudu',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
