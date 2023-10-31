from django.shortcuts import render, HttpResponse
import json

def register(request):
    if(request.method=="GET"):
        return render(request, "register.html")
    elif(request.method=="POST"):
        return HttpResponse("lol")

def login(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")


