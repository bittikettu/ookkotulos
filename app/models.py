"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User,Group,Permission,AbstractUser
import datetime
from django.utils import timezone

class Person(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    events = models.ManyToManyField('Event', through='EventsJoined',blank=True,default=None)

    def __str__(self):
        self.username
        if len(self.first_name) == 0:
            return f'{self.username}'
        else:
            return f'{self.first_name} {self.last_name}'

class EventTypes(models.Model):
    name = models.CharField(max_length=128)
    badgecolor = models.CharField(max_length=20,default="bg-success")

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=128)
    creator = models.ForeignKey(Person,null=True, on_delete=models.SET_NULL,default=None, related_name='creator')
    members = models.ManyToManyField(Person, through='EventsJoined',blank=True,default=None)
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
    date_joined = models.DateField(default=timezone.now)
    cancel = models.BooleanField(name='Peruutus', default=False)
    join = models.BooleanField(default=False)
    date_cancel = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = [['person', 'event']]

    def cancelevent(self):
        self.cancel = True
        self.join = False
        self.date_cancel = datetime.date.today()
        print("Cancel event")

    def jointoevent(self):
        self.join = True
        self.cancel = False
        self.date_joined = datetime.date.today()
        print("Joining to event")

    def __str__(self):
        return f'{self.event.name} {self.person.username}'


