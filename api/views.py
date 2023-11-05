from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team, Todo, UsersInTeams

User = get_user_model()

TODO_STATUS = ["TODO", "PROGRESS", "COMPLETE"]
TODO_PRIORITY = ["LOW", "MEDIUM", "HIGH"]
class ToDoView(APIView):
    def get(self, request, format=None):
        return Response("GET")
    
    def post(self, request, format=None):
        try:
            if(type(request.user)==AnonymousUser):
                return Response({"error":"Unauthorized"}, status=401)
            team_id = request.data["team"]
            title = request.data["title"]
            body = request.data["body"]
            status = request.data["status"]
            status = TODO_STATUS[status]
            priority = request.data["priority"]
            priority = TODO_PRIORITY[priority]
            assigned_to = request.data["assigned_to"]

            team = Team.objects.get(pk=team_id)
            if not (team.leader == request.user ):
                return Response({"error":"Unauthorized"}, status=401)

            user = User.objects.get(pk=assigned_to)
            check_existence = UsersInTeams.objects.filter(user=user, team=team)
            if(not check_existence):
                return Response({"error":"Bad Request"}, status=400)
            new_todo = Todo.objects.create(
                title=title,
                body=body,
                status=status,
                priority=priority,
                assigned_to=user,
                team=team
            )
            new_todo.save()
            return Response({"success":"Created new todo"}, status=200)
        except BaseException as e:
            print(e)
            return Response({"error":"Internal Server Error"}, status=500)