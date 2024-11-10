# Django imports
from django.shortcuts import render
from .serializers import WAFSerializer
from .models import WAF
from requests import get, post

# Rest Framework imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Docker imports
import docker

# CSV imports
import csv

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
    def get_combined_results(self, request):
        conventional_results = WAFView.get_conventional_results(self, request)
        unconventional_results = WAFView.get_unconventional_results(self, request)

        print(f'Conventional: {conventional_results.data}')
        print(f'Unconventional: {unconventional_results.data}')

        tpr = (3*conventional_results.data.get('tpr') + unconventional_results.data.get('tpr')) / 4
        tnr = (3*conventional_results.data.get('tnr') + unconventional_results.data.get('tnr')) / 4

        print(f'TPR: {tpr}, TNR: {tnr}')

        return Response({'balanced': {'time': 0.0, 'tpr': tpr, 'tnr': tnr}, 'conventional': conventional_results.data, 'unconventional': unconventional_results.data})
    
    @action(detail=False, methods=['post'])
    def get_conventional_results(self, request):
        id = request.data.get('id')
        tp, fp, tn, fn = 0, 0, 0, 0

        with open('waf/datasets/csic.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            csic_data = [row for row in csv_reader]

        for row in csic_data:
            HEADERS = {'User-Agent': row['User-Agent']}
            if row['Method'] == 'GET':
                PARAMS = {'get-query': row['GET-Query']}
                if row['URI'][0] == '/':
                    response = get(f'http://localhost:500{id}{row['URI']}', params=PARAMS, headers=HEADERS)
                else:
                    response = get(f'http://localhost:500{id}/{row['URI']}', params=PARAMS, headers=HEADERS)
            else:
                DATA = {'post-data': row['POST-Data']}
                if row['URI'][0] == '/':
                    response = post(f'http://localhost:500{id}{row['URI']}', data=DATA, headers=HEADERS)
                else:
                    response = post(f'http://localhost:500{id}/{row['URI']}', data=DATA, headers=HEADERS)
            if response.status_code != 403:
                if row['Class'] == 'Anomalous':
                    fp += 1
                else:
                    tp += 1
            else:
                if row['Class'] == 'Anomalous':
                    tn += 1
                else:
                    fn += 1

        tpr = tp / (tp + fn) * 100
        tnr = tn / (tn + fp) * 100

        return Response({'time': 0.0, 'tpr': tpr, 'tnr': tnr})
    
    @action(detail=False, methods=['post'])
    def get_unconventional_results(self, request):
        id = request.data.get('id')
        container_name = request.data.get('waf_container_name')

        tpr, tnr = 0, 0
        tp, fp, tn, fn = 0, 0, 0, 0
        if container_name == 'TIREDFUL_WAF':
            with open('waf/datasets/tiredful_testing.csv', 'r') as file:
                csv_reader = csv.DictReader(file)
                data = [row for row in csv_reader]

            for row in data:
                if row['Method'] == 'GET':
                    response = get(f'http://localhost:500{id}{row['URI']}', cookies={'token': row['Cookie']})
                else:
                    response = post(f'http://localhost:500{id}{row['URI']}', cookies={'token': row['Cookie']})

                if response.status_code != 403:
                    if row['Class'] == 'Anomalous':
                        fp += 1
                    else:
                        tp += 1
                else:
                    if row['Class'] == 'Anomalous':
                        tn += 1
                    else:
                        fn += 1
        elif container_name == 'CTF_WAF':
            print('CTF_WAF')
            with open('waf/datasets/ctf_testing.csv', 'r') as file:
                csv_reader = csv.DictReader(file)
                data = [row for row in csv_reader]

            print('Finished reading file')

            for row in data:            
                if row['Method'] == 'GET':
                    response = get(f'http://localhost:500{id}{row['URI']}', cookies={'token': row['Cookie']})
                else:
                    response = post(f'http://localhost:500{id}{row['URI']}', cookies={'token': row['Cookie']})
                
                if response.status_code != 403:
                    if row['Class'] == 'Anomalous':
                        fp += 1
                    else:
                        tp += 1
                else:
                    if row['Class'] == 'Anomalous':
                        tn += 1
                    else:
                        fn += 1
        elif container_name == 'DVWA_WAF':
            with open('waf/datasets/dvwa_testing.csv', 'r') as file:
                csv_reader = csv.DictReader(file)
                data = [row for row in csv_reader]

            for row in data:
                if row['Method'] == 'GET':
                    response = get(f'http://localhost:500{id}{row['URI']}')
                else:
                    response = post(f'http://localhost:500{id}{row['URI']}')

                if response.status_code != 403:
                    if row['Class'] == 'Anomalous':
                        fp += 1
                    else:
                        tp += 1
                else:
                    if row['Class'] == 'Anomalous':
                        tn += 1
                    else:
                        fn += 1

        tpr = tp / (tp + fn) * 100
        tnr = tn / (tn + fp) * 100
            
        return Response({'time': 0.0, 'tpr': tpr, 'tnr': tnr})