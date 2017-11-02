# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response

from buffer.models import Text

BufferType = str


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world! Buffers are waiting!")
  
  
def read(request: HttpRequest, buffer_id: BufferType) -> HttpResponse:
    return render_to_response('read_template.html', {'buffer_id': buffer_id})


def edit(request: HttpRequest, buffer_id: BufferType) -> HttpResponse:
    return render_to_response('edit_template.html', {'buffer_id': buffer_id})


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
    return get_text


def update(id, text, name):
    '''Updates record in bd, 3 args - id, text and name'''
    upd_text = Text(id = id, text = text, name = name)
    upd_text.save()


def lookup_private(token):
    obj = Text.objects.filter(private = token)
    if obj:
         return obj[0].text
    else:
         raise ValueError('Private key is not valid')


def lookup_public(token):
    obj = Text.objects.filter(public = token)
    if obj:
         return obj[0].text
    else:
         raise ValueError('Public key is not valid')


def gen(n):
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits)
                                 for _ in range(n))
