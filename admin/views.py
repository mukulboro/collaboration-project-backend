from django.http import HttpResponse, JsonResponse

def index(request):
    test = {
        "test" : "test"
    }
    return JsonResponse(test)
