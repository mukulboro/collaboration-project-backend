from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from api.models import ProjectMedia, Project, UsersInProjects, Document

User = get_user_model()


class ProjectMediaView(APIView):
    def get(self, request, format=None):
        parser_classes = [MultiPartParser]

        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            project_id = request.data["project"]
            project_medias = ProjectMedia.objects.filter(project=project_id).order_by(
                "-created_at"
            )
            media_list = []
            for media in project_medias:
                media_list.append(
                    {
                        "id": media.pk,
                        "name": media.image.name,
                        "image_slug": media.image.url,
                        "thumbnail_slug": media.image_thumbnail.url,
                        "created_at": media.created_at,
                    }
                )
            return Response(media_list, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)

    def post(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            project_id = request.data["project"]
            image = request.FILES["image"]
            project = Project.objects.get(pk=project_id)
            check_existence = UsersInProjects.objects.filter(
                project=project, user=request.user
            )
            if not check_existence:
                return Response({"error": "Unauthorized"}, status=401)

            project_media = ProjectMedia.objects.create(project=project, image=image)
            project_media.save()
            return Response({"success": "Created new project media"})
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)

    def delete(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            media_id = request.data["media"]
            project_media = ProjectMedia.objects.filter(pk=media_id)
            if not project_media:
                return Response({"error": "Bad Request"}, status=401)
            user_in_project = UsersInProjects.objects.filter(
                user=request.user, project=project_media.project
            )
            if not user_in_project:
                return Response({"error": "Unauthorized"}, status=401)
            project_media.delete()

            return Response({"success": "Deleted Media"})
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)


class DocumentView(APIView):
    def get(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            project_id = request.data["project"]
            project = Project.objects.get(pk=project_id)
            user_in_project = UsersInProjects.objects.filter(
                project=project_id, user=request.user
            )
            if not user_in_project:
                return Response({"error": "Unauthorized"}, status=401)

            documents = Document.objects.filter(project=project).order_by("-created_at")
            document_list = []

            for document in documents:
                document_list.append(
                    {
                        "id": document.pk,
                        "title": document.title,
                        "body": document.body,
                        "created_at": document.created_at,
                    }
                )
            return Response(document_list, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)

    def post(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            project_id = request.data["project"]
            project = Project.objects.get(pk=project_id)
            title = request.data["title"]
            body = request.data["body"]
            user_in_project = UsersInProjects.objects.filter(
                project=project_id, user=request.user
            )
            if not user_in_project:
                return Response({"error": "Unauthorized"}, status=401)

            new_document = Document(project=project, title=title, body=body)
            new_document.save()
            return Response({"success": "Created new document"}, status=200)
        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)

    def delete(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            document_id = request.data["document"]
            document = Document.objects.get(pk=document_id)
            user_in_project = UsersInProjects.objects.filter(
                project=document.project.pk, user=request.user
            )
            if not user_in_project:
                return Response({"error": "Unauthorized"}, status=401)
            document.delete()
            return Response({"success":"Deleted Document"}, status=200)

        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)
        
    def put(self, request, format=None):
        try:
            if type(request.user) == AnonymousUser:
                return Response({"error": "Unauthorized"}, status=401)
            document_id = request.data["document"]
            title = request.data["title"]
            body = request.data["body"]
            document = Document.objects.get(pk=document_id)
            user_in_project = UsersInProjects.objects.filter(
                project=document.project.pk, user=request.user
            )
            if not user_in_project:
                return Response({"error": "Unauthorized"}, status=401)
            document.title = title
            document.body = body
            document.save()
            return Response({"success":"Updated Document"}, status=200)

        except BaseException as e:
            print(e)
            return Response({"error": "Internal Server Error"}, status=500)
