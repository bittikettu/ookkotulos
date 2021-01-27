"""
Definition of urls for modeltest2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
import django.contrib.auth.forms


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path("register/", views.register, name="register"),  # <-- added
    path('cancelevent/<str:pk>/', views.cancelevent, name='cancelevent'),
    path('joinevent/<str:pk>/', views.joinevent, name='joinevent'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
