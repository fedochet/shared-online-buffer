# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from buffer.models import Text

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest
import random
import string


def index(request: HttpRequest) -> HttpResponse:
    print(get(1)['private'])
    #print(lookup_public('wggjioe'))
    print(lookup_private('XwW8HbCxu'))
    return HttpResponse("Hello, world! Buffers are waiting!")
  
  
def read(request: HttpRequest) -> HttpResponse:
    return render_to_response('read_template.html')


def edit(request: HttpRequest) -> HttpResponse:
    return render_to_response('edit_template.html')

def create(text, name):
    '''Creates record in bd, 2 args - text and name. Generate priv-pub links
       Returns id of new record!'''
    public = gen(6)
    private = gen(8)
    new_text = Text(text = text, name = name, public = public, private = private)
    new_text.save()
    return new_text.id

def get(id):
    '''Reads record in bd. Returns dict with keys: id, text and name'''
    get_text = Text.objects.get(id = id)
    rec = {'id' : get_text.id, 
           'text' : get_text.text,
           'name' : get_text.name,
           'private' :  get_text.private,
           'public' :  get_text.public,
           }
    return(rec)

def update(id, text, name):
    '''Updates record in bd, 3 args - id, text and name'''
    upd_text = Text(id = id, text = text, name = name)
    upd_text.save()

def lookup_private(token):
    obj = Text.objects.filter(private = token)
    if obj:
         return obj[0].text
    else:
         return "Private key is not valid"

def lookup_public(token):
    obj = Text.objects.filter(public = token)
    if obj:
         return obj[0].text
    else:
         return "Public key is not valid"

def gen(n):
    return ''.join(random.choice(string.ascii_uppercase + 
                                 string.ascii_lowercase + 
                                 string.digits)
                                 for _ in range(n))
    
    
