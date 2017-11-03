# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Text(models.Model):
    text = models.TextField(max_length=1000)
    name = models.CharField(max_length=60)
    private = models.CharField(max_length=8, unique = True, blank = True)
    public = models.CharField(max_length=6, unique = True,  blank = True)

    def __str__(self):
        return self.name
