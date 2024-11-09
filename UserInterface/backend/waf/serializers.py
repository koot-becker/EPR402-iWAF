from rest_framework import serializers
from .models import WAF

class WAFSerializer(serializers.ModelSerializer):
    class Meta:
        model = WAF
        fields = ('id', 'name', 'description', 'waf_address', 'app_address', 'waf_container_name', 'app_container_name', 'app_container_image_name', 'app_internal_port_number', 'app_external_port_number', 'total_requests', 'average_time', 'allowed_requests', 'blocked_requests', 'app_enabled', 'waf_enabled', 'settings', 'rules', 'results')