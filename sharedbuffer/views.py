# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response

from buffer.models import Text


def index(request: HttpRequest) -> HttpResponse:
    texts_count = len(Text.objects.all())
    if texts_count < 5:
         links = Text.objects.all()
    else:
         links = Text.objects.all()
    return render_to_response('index.html', {'links': links})

