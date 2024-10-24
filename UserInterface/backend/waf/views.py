# Django imports
from django.shortcuts import render
from .serializers import WAFSerializer
from .models import WAF
from requests import get

# Rest Framework imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Docker imports
import docker

class WAFView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    serializer_class = WAFSerializer
    queryset = WAF.objects.all()

    @action(detail=False, methods=['post'])
    def start_waf(self, request):
        data = request.data
        id = data.get('id')
        url = data.get('app_address')
        waf_container_name = data.get('waf_container_name')
        client = docker.from_env()
        try:
            client.containers.get(waf_container_name).start()
        except:
            client.containers.run('waf', f'--id {id} --url {url}', network_mode='host', name=waf_container_name, detach=True)
        waf = WAF.objects.get(id=id)
        waf.waf_enabled = True
        waf.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def stop_waf(self, request):
        data = request.data
        id = data.get('id')
        waf_container_name = data.get('waf_container_name')
        client = docker.from_env()
        container = client.containers.get(waf_container_name)
        container.stop()
        waf = WAF.objects.get(id=id)
        waf.waf_enabled = False
        waf.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def start_app(self, request):
        data = request.data
        id = data.get('id')
        client = docker.from_env()
        app_container_name = data.get('app_container_name')
        app_container_image_name = data.get('app_container_image_name')
        app_internal_port_number = data.get('app_internal_port_number')
        app_external_port_number = data.get('app_external_port_number')
        if app_container_name == 'dvwa-dvwa-1':
            client.containers.get(app_container_name).start()
            client.containers.get('dvwa-db-1').start()
        else:
            try:
                client.containers.get(app_container_name).start()
            except:
                client.containers.run(app_container_image_name, ports={f'{app_internal_port_number}/tcp': app_external_port_number}, name=app_container_name, detach=True)
        app = WAF.objects.get(id=id)
        app.app_enabled = True
        app.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def stop_app(self, request):
        data = request.data
        id = data.get('id')
        client = docker.from_env()
        app_container_name = data.get('app_container_name')
        container = client.containers.get(app_container_name)
        container.stop()
        app = WAF.objects.get(id=id)
        app.app_enabled = False
        app.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def get_balanced_results(self, request):
        id = request.data.get('id')
        api_url = f'http://localhost:800{id}/waf_api/get_balanced_results/'
        response = get(api_url)
        balanced_results = response.json()
        return Response(balanced_results)
    
    @action(detail=False, methods=['post'])
    def get_conventional_results(self, request):
        id = request.data.get('id')
        api_url = f'http://localhost:800{id}/waf_api/get_conventional_results/'
        response = get(api_url)
        conventional_results = response.json()
        return Response(conventional_results)
    
    @action(detail=False, methods=['post'])
    def get_unconventional_results(self, request):
        id = request.data.get('id')
        api_url = f'http://localhost:800{id}/waf_api/get_unconventional_results/'
        response = get(api_url)
        unconventional_results = response.json()
        return Response(unconventional_results)