from django import http
from django.shortcuts import render
from core.models import Material

def index(request):
    context = {
        'materials': Material.objects.all(),
    }
    return render(request, 'index.html', context)
