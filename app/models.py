"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User,Group,Permission,AbstractUser
import datetime

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    events = models.ManyToManyField('Event', through='EventsJoined')

    class Meta:
        ordering = ['user']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user})'

class EventTypes(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='EventsJoined')
    type = models.ForeignKey(EventTypes, on_delete=models.CASCADE)
    max = models.SmallIntegerField()
    date = models.DateTimeField()
    description = models.TextField(max_length=500,default='')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date} {self.type.name} {self.name}'

class EventsJoined(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateField()
    cancel = models.BooleanField(name='Peruutus', default=False)
    join = models.BooleanField(default=False)
    date_cancel = models.DateField(null = True)

    class Meta:
        unique_together = [['person', 'event']]

    def cancelevent(self):
        self.cancel = True
        self.join = False
        self.date_cancel = datetime.date.today()

    def jointoevent(self):
        self.join = True
        self.cancel = False
        self.date_joined = datetime.date.today()
        print("Joining to event")


    def __str__(self):
        return self.event.name

