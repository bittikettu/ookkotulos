import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from .models import *
from .forms import *
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from json import JSONEncoder
from uuid import UUID
JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)

    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_newdefault

def logshit(request,object,message,actionflag):
    LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(object).pk,
                object_id=object.id,
                object_repr=str(object),
                change_message=serializers.serialize('json', [ object, ]),
                action_flag=actionflag)# if create else CHANGE)

def getEpochFromUUID(uuid):
    return uuid.time/1e7-12219292800
