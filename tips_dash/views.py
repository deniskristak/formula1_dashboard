# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, 'dash_index.html')
