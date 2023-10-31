from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from cdn.models import ProfilePicture
from .models import EndUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        try:
            username = request.data["username"]
            password = request.data["password"]
            profile_pic = request.FILES["profile_pic"]
            first_name = request.data["first_name"]
            last_name = request.data["first_name"]
            email = request.data["email"]
            role = "USER"

            hashed_password = make_password(password)

            user = User.objects.create(
                username=username,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                role = role
            )
            user.save()

            pp = ProfilePicture.objects.create(
                image_path = profile_pic
            )
            pp.save()

            end_user = EndUser(user=user, profile_picture=pp)
            end_user.save()
            
            return Response({
                "success" : "Created New User With Credentials"
            }, status=200)
        except IntegrityError as e:
            return Response({"error":"Username already in use"}, status=400)
        except BaseException as e:
            print(e)
            return Response({"error":"Internal Server Error"}, status=500)


class LoginView(APIView):
    def post(self, request, format=None):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({"error":"Invalid credentials"}, status=401)
            token = Token.objects.create(user=user)
            return Response({"success":"Login successful", "token":token.key})
        except IntegrityError as e:
            token = Token.objects.get(user=user)
            token.delete()
            new_token = Token.objects.create(user=user)
            return Response({"success":"Login successful", "token":new_token.key})
            
        except BaseException as e:
            print(e.__str__)
            return Response({"error":"Internal Server Error"}, status=500)
