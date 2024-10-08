from django.shortcuts import render
from rest_framework import viewsets
from .serializers import WAFSerializer
from .models import WAF

# Create your views here.

class WAFView(viewsets.ModelViewSet):
    serializer_class = WAFSerializer
    queryset = WAF.objects.all()