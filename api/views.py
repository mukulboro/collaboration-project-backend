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
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            team_id = request.data["team"]
            team = Team.objects.get(pk=team_id)
            user_in_team = UsersInTeams.objects.filter(team=team, user=request.user)
            if not user_in_team:
                return Response({"error": "Unauthorized"}, status=401)
            todos = Todo.objects.filter(team=team).order_by("-created_at")
            payload = []
            for todo in todos:
                payload.append(
                    {
                        "id": todo.pk,
                        "title": todo.title,
                        "body": todo.body,
                        "priority": todo.priority,
                        "status": todo.status,
                        "assigned_to": todo.assigned_to.username,
                        "created_at": todo.created_at,
                    }
                )
            return Response(payload, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)

    def post(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            team_id = request.data["team"]
            title = request.data["title"]
            body = request.data["body"]
            status = request.data["status"]
            status = TODO_STATUS[status]
            priority = request.data["priority"]
            priority = TODO_PRIORITY[priority]
            assigned_to = request.data["assigned_to"]

            team = Team.objects.get(pk=team_id)
            if not (team.leader == request.user):
                return Response({"error": "Unauthorized"}, status=401)

            user = User.objects.get(pk=assigned_to)
            check_existence = UsersInTeams.objects.filter(user=user, team=team)
            if not check_existence:
                return Response({"error": "Bad Request"}, status=400)
            new_todo = Todo.objects.create(
                title=title,
                body=body,
                status=status,
                priority=priority,
                assigned_to=user,
                team=team,
            )
            new_todo.save()
            return Response({"success": "Created new todo"}, status=200)
        except BaseException as e:
            return Response({"error": "Internal Server Error"}, status=500)

    def delete(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            todo_id = request.data["todo"]
            todo = Todo.objects.get(pk=todo_id)
            team = Team.objects.get(pk=todo.team.pk)
            if not (team.leader == request.user):
                return Response({"error": "Unauthorized"}, status=200)

            todo.delete()
            return Response({"success": "Created Deleted Todo"}, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)
