# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from buffer.models import Text

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world! Buffers are waiting!")
  
  
def read(request: HttpRequest) -> HttpResponse:
    return render_to_response('read_template.html')


def edit(request: HttpRequest) -> HttpResponse:
    return render_to_response('edit_template.html')

def create(text, name):
    '''Creates record in bd, 2 args - text and name. 
       Returns id of new record!'''
    new_text = Text(text = text, name = name)
    new_text.save()
    return new_text.id

def get(id):
    '''Reads record in bd. Returns dict with keys: id, text and name'''
    get_text = Text.objects.get(id = id)
    rec = {'id' : get_text.id, 
           'text' : get_text.text,
           'name' : get_text.name}
    return(rec)

def update(id, text, name):
    '''Updates record in bd, 3 args - id, text and name'''
    upd_text = Text(id = id, text = text, name = name)
    upd_text.save()

    
    
    
