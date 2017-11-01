# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world! Buffers are waiting!")


def read(request: HttpRequest) -> HttpResponse:
    return render_to_response('read_template.html')


def edit(request: HttpRequest) -> HttpResponse:
    return render_to_response('edit_template.html')
