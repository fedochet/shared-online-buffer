# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from buffer.models import Text


def index(request):
    #all_entries = Text.objects.all()
    #print(all_entries)
    return HttpResponse("Hello, world! Buffers are waiting!")


def read(request):
    return render_to_response('read_template.html')

def edit(request):
    return render_to_response('edit_template.html')
