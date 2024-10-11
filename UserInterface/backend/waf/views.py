# Django imports
from django.shortcuts import render
from .serializers import WAFSerializer
from .models import WAF

# Rest Framework imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Docker imports
import docker

class WAFView(viewsets.ModelViewSet):
    serializer_class = WAFSerializer
    queryset = WAF.objects.all()

    @action(detail=False, methods=['get','post'])
    def start_waf(self, request, app):
        client = docker.from_env()
        client.containers.run('waf', ports={'5000/tcp': 5001}, name="WAF", detach=True)
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get','post'])
    def stop_waf(self, request):
        client = docker.from_env()
        container = client.containers.get('WAF')
        container.stop()
        container.remove()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get','post'])
    def start_app(self, request):
        client = docker.from_env()
        client.containers.run('ctf-jwt-token', ports={'8080/tcp': 8001}, name="CTF-JWT", detach=True)
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['get','post'])
    def stop_app(self, request):
        client = docker.from_env()
        container = client.containers.get('CTF-JWT')
        container.stop()
        container.remove()
        return Response({'status': 'success'})