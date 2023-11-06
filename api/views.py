from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team, Todo, UsersInTeams, UsersInProjects, Announcement

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
            return Response({"success": "Deleted Todo"}, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)

    def patch(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            todo_id = request.data["todo"]
            status = request.data["status"]
            status = TODO_STATUS["status"]
            todo = Todo.objects.get(pk=todo_id)
            team = Team.objects.get(pk=todo.team.pk)
            check_existence = UsersInTeams.objects.filter(team=team, user=request.user)
            if not check_existence:
                return Response({"error": "Unauthorized"}, status=401)

            todo.status = status
            todo.save()
            return Response({"success": "Updated Todo"}, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)


class DashboardView(APIView):
    def get(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            projects = UsersInProjects.objects.filter(user=request.user)
            announcement_list = []

            for project in projects:
                announcements = Announcement.objects.filter(
                    project=project.project
                ).order_by("-created_at")
                for announcement in announcements:
                    announcement_list.append(
                        {
                            "project": project.project.name,
                            "project_id": project.project.pk,
                            "id" : announcement.pk,
                            "title" : announcement.title,
                            "body" : announcement.body,
                            "created_at" : announcement.created_at
                        }
                    )

            todo_list = []
            todos = Todo.objects.filter(assigned_to=request.user, status="TODO").order_by("-created_at")
            for todo in todos:
                todo_list.append({
                    "id" : todo.pk,
                    "title" : todo.title,
                    "body" : todo.body,
                    "status" : todo.status,
                    "priority" : todo.priority,
                    "created_at" : todo.created_at,
                    "team" : todo.team.name,
                    "team_id" : todo.team.pk,
                    "project" : todo.team.project.name,
                    "project_id" : todo.team.project.pk
                })
            return Response({
                "announcements": announcement_list,
                "todos" : todo_list
            }, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)
        
class ProjectsView(APIView):
    def get(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            
        except BaseException as e:
            print(e)
            return Response({"error":"Internal Server Error"}, status=500)
