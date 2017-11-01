# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from buffer.models import Text


def index(request):
    #all_entries = Text.objects.all()
    #print(all_entries)
    return HttpResponse("Hello, world! Buffers are waiting!")
