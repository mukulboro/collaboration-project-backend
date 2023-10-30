from django.shortcuts import render, HttpResponse

def index(request):
    return HttpResponse("API")

# Create your views here.
