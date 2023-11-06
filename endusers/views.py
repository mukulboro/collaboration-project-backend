from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from cdn.models import ProfilePicture
from .models import EndUser
from api.models import UsersInProjects, UsersInTeams, Team
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
                role=role,
            )
            user.save()

            pp = ProfilePicture.objects.create(image_path=profile_pic)
            pp.save()

            end_user = EndUser(user=user, profile_picture=pp)
            end_user.save()

            return Response(
                {"success": "Created New User With Credentials"}, status=200
            )
        except IntegrityError as e:
            return Response({"error": "Username already in use"}, status=400)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)


class LoginView(APIView):
    def post(self, request, format=None):
        try:
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({"error": "Invalid credentials"}, status=401)
            end_user = EndUser.objects.get(user=user)
            pp = end_user.profile_picture
            pp_url = str(pp.image_path.url)
            token = Token.objects.create(user=user)
            return Response(
                {
                    "success": "Login successful",
                    "username": user.username,
                    "userID": user.pk,
                    "token": token.key,
                    "profile_picture": pp_url,
                }
            )
        except IntegrityError as e:
            token = Token.objects.get(user=user)
            token.delete()
            new_token = Token.objects.create(user=user)
            return Response(
                {
                    "success": "Login successful",
                    "username": user.username,
                    "userID": user.pk,
                    "token": new_token.key,
                    "profile_picture": pp_url,
                }
            )
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)


class UserMetadataView(APIView):
    def get(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            user_in_project = UsersInProjects.objects.filter(user=request.user)
            projects = []
            for relationship in user_in_project:
                teams = Team.objects.filter(project=relationship.project.pk)
                team_list = []
                for team in teams:
                    check_existence = UsersInTeams.objects.filter(team=team, user=request.user)
                    if check_existence:
                        team_list.append({
                            "id": check_existence[0].team.pk,
                            "name" : check_existence[0].team.name,
                            "isLead" : check_existence[0].team.leader.username == request.user.username
                        })
                projects.append(
                    {
                        "project_id": relationship.project.pk,
                        "project_name": relationship.project.name,
                        "teams" : team_list
                    }
                )
            return Response(projects)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)
