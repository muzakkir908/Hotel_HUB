from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")  # return 200 OK
