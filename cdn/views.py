from django.shortcuts import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import renderers
from .models import ProfilePicture
from endusers.models import EndUser
from PIL import Image
import os

class CustomRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

class ProfilePictureView(APIView):

    def get(self, request, format=None):
        end_user = EndUser.objects.get(user=request.user)
        profile_picture = ProfilePicture.objects.get(image_path = end_user.profile_picture.image_path)
        img_name = profile_picture.image_path.name
        return HttpResponseRedirect(f"/{img_name}")
