# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response, redirect, render

from buffer.models import Text


def index(request: HttpRequest) -> HttpResponse:
    texts_count = len(Text.objects.all())
    if texts_count < 5:
         links = Text.objects.all()
    else:
         links = Text.objects.all()
    return render_to_response('index.html', {'links': links})
  
  
def read(request: HttpRequest, public_token: str) -> HttpResponse:
    if lookup_public(public_token):
         return render_to_response('read_template.html', {'name': lookup_public(public_token).name})
    else:
         return server_error('Public key is not valid')


def edit(request: HttpRequest, private_token: str) -> HttpResponse:
    if lookup_private(private_token):
         obj = lookup_private(private_token)
         context = {'public_key': obj.public,
                    'name': obj.name}
         return render_to_response('edit_template.html', context=context)
    else:
         return server_error('Private key is not valid')


def new(request: HttpRequest) -> HttpResponse:
    if 'name' in request.GET.keys() :
        new_id = create('', request.GET['name'])
        created_record = get(new_id)
    else:
        new_id = create('', 'New Buffer')
        created_record = get(new_id)
    return redirect('/buffer/edit/' + created_record.private)


def create(text, name):
    '''Creates record in bd, 2 args - text and name. Generate priv-pub links
       Returns id of new record!'''
    public = gen(6)
    private = gen(8)
    new_text = Text(text=text, name=name, public=public, private=private)
    new_text.save()
    return new_text.id


def get(id):
    '''Reads record in bd. Returns dict with keys: id, text and name'''
    try:
        get_text = Text.objects.get(id=id)
        return get_text
    except:
        return server_error("No such id")
       

def update(id, text, name):
    '''Updates record in bd, 3 args - id, text and name'''
    try:
       upd_text = Text(id=id, text=text, name=name)
       upd_text.save()
    except:
       return server_error("No such id")


def lookup_private(token) -> Text:
    obj = Text.objects.filter(private=token)    
    if obj:
        return obj[0]
    else:
        return None




def lookup_public(token) -> Text:
    obj = Text.objects.filter(public=token)
    if obj:
        return obj[0]
    else:
        return None
      

def gen(n):
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits)
                   for _ in range(n))

#Error handlers
def server_error(msg):
    response = render_to_response(
    'errors/500.html', {'msg': msg})
    response.status_code = 500
    return response
