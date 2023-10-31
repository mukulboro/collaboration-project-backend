from django.shortcuts import render, HttpResponse
from django.http import FileResponse

def index(request):
    return HttpResponse("CDN")

# Create your views here.
