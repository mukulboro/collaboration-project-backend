from django.shortcuts import render, HttpResponse

def index(request):
    return HttpResponse("ADMINDASH")

# Create your views here.
