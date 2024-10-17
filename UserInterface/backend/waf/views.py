# Django imports
from django.shortcuts import render
from .serializers import WAFSerializer
from .models import WAF

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
        client = docker.from_env()
        match id:
            case 1:
                try:
                    client.containers.get('TIREDFUL_WAF').start()
                except:
                    client.containers.run('waf', f'--id 1 --url {url}', network_mode='host', name="TIREDFUL_WAF", detach=True)

            case 2:
                try:
                    client.containers.get('CTF_WAF').start()
                except:
                    client.containers.run('waf', f'--id 2 --url {url}', network_mode="host", name="CTF_WAF", detach=True)
            case 4:
                try:
                    client.containers.get('DVWA_WAF').start()
                except:
                    client.containers.run('waf', f'--id 3 --url {url}', network_mode='host', name="DVWA_WAF", detach=True)
            case _:
                return Response({'status': 'unknown action'}, status=400)

        waf = WAF.objects.get(id=id)
        waf.waf_enabled = True
        waf.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def stop_waf(self, request):
        data = request.data
        id = data.get('id')
        url = data.get('app_address')
        client = docker.from_env()
        match id:
            case 1:
                container = client.containers.get('TIREDFUL_WAF')
            case 2:
                container = client.containers.get('CTF_WAF')
            case 4:
                container = client.containers.get('DVWA_WAF')
            case _:
                return Response({'status': 'unknown action'}, status=400)
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
        match id:
            case 1:
                try:
                    client.containers.get('TIREDFUL').start()
                except:
                    client.containers.run('tiredful', ports={'8000/tcp': 8001}, name="TIREDFUL", detach=True)
            case 2:
                try:
                    client.containers.get('CTF-JWT').start()
                except:
                    client.containers.run('ctf-jwt-token', ports={'8080/tcp': 8002}, name="CTF-JWT", detach=True)
            case 4:
                try:
                    client.containers.get('dvwa-dvwa-1').start()
                except:
                    client.containers.run('ghcr.io/digininja/dvwa:latest', ports={'80/tcp': 8003}, name="dvwa-dvwa-1", detach=True)

                try:
                    client.containers.get('dvwa-db-1').start()
                except:
                    client.containers.run('mariadb:10', name="dvwa-db-1", detach=True)
            case _:
                return Response({'status': 'unknown action'}, status=400)
        app = WAF.objects.get(id=id)
        app.app_enabled = True
        app.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def stop_app(self, request):
        data = request.data
        id = data.get('id')
        client = docker.from_env()
        match id:
            case 1:
                container = client.containers.get('TIREDFUL')
            case 2:
                container = client.containers.get('CTF-JWT')
            case 4:
                container = client.containers.get('DVWA')
            case _:
                return Response({'status': 'unknown action'}, status=400)
        container.stop()
        app = WAF.objects.get(id=id)
        app.app_enabled = False
        app.save()
        return Response({'status': 'success'})