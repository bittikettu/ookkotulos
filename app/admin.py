from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group,Permission,AbstractUser
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

class EventsInline(admin.StackedInline):
    model = EventsJoined
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    inlines = (EventsInline,)

class EventAdmin(admin.ModelAdmin):
    inlines = (EventsInline,)

admin.site.register(LogEntry)
admin.site.register(Person, PersonAdmin)
admin.site.register(EventTypes)
admin.site.register(EventsJoined)
admin.site.register(Event,EventAdmin)