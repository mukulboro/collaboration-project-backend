from django.shortcuts import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import renderers
from .models import ProfilePicture
from endusers.models import EndUser
from PIL import Image
import os

