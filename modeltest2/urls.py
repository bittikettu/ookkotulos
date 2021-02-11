"""
Definition of urls for modeltest2.
"""

from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
import django.contrib.auth.forms


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path("register/", views.register, name="register"),
    path("creategroup/", views.creategroup, name="creategroup"),
    path("joingroup/", views.joingroup, name="joingroup"),
    path("user/", views.user, name="user"),
    path("addevent/", views.addevent, name="addevent"),
    path('eventsettings/<str:pk>/', views.eventsettings, name='eventsettings'),
    path('eventremove/<str:pk>/', views.eventremove, name='eventremove'),
    path('cancelevent/<str:pk>/', views.cancelevent, name='cancelevent'),
    path('joinevent/<str:pk>/', views.joinevent, name='joinevent'),
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
