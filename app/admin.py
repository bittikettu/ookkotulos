from django.contrib import admin
# from django.apps import apps
# from django.contrib.auth.models import Group,Permission,AbstractUser
from django.contrib.auth.admin import UserAdmin
from .models import Person, EventTypes, EventsJoined, Event
from django.contrib.admin.models import LogEntry


class EventsInline(admin.StackedInline):
    model = EventsJoined
    extra = 1

# class PersonAdmin(UserAdmin):
#    inlines = (EventsInline,)


class EventAdmin(admin.ModelAdmin):
    inlines = (EventsInline,)


admin.site.register(LogEntry)
admin.site.register(Person, UserAdmin)
admin.site.register(EventTypes)
admin.site.register(EventsJoined)
admin.site.register(Event, EventAdmin)
