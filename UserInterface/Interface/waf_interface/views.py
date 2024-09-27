from django.http import HttpResponse
from django.template import loader
from .models import WebApplication

def web_applications(request):
    web_applications = WebApplication.objects.all().values()
    template = loader.get_template('web_applications.html')
    context = {
        'web_applications': web_applications
    }
    return HttpResponse(template.render(context, request))

def web_app_1(request):
    template = loader.get_template('web_app_1.html')
    return HttpResponse(template.render())

def web_app_2(request):
    template = loader.get_template('web_app_2.html')
    return HttpResponse(template.render())

def web_app_3(request):
    template = loader.get_template('web_app_3.html')
    return HttpResponse(template.render())
