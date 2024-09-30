from django.http import HttpResponse
from django.template import loader
from .models import WebApplication

def main(request):
    web_applications = WebApplication.objects.all().values()
    template = loader.get_template('main.html')
    context = {
        'web_applications': web_applications
    }
    return HttpResponse(template.render(context, request))

def web_app_1(request):
    web_application = WebApplication.objects.all()[0]	
    template = loader.get_template('web_app_1.html')
    context = {
        'web_application': web_application
    }
    return HttpResponse(template.render(context, request))

def web_app_2(request):
    web_application = WebApplication.objects.all()[0]	
    template = loader.get_template('web_app_2.html')
    context = {
        'web_application': web_application
    }
    return HttpResponse(template.render(context, request))

def web_app_3(request):
    web_application = WebApplication.objects.all()[0]	
    template = loader.get_template('web_app_3.html')
    context = {
        'web_application': web_application
    }
    return HttpResponse(template.render(context, request))
