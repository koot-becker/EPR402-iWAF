from rest_framework import serializers
from .models import WAF

class WAFSerializer(serializers.ModelSerializer):
    class Meta:
        model = WAF
        fields = ('id', 'name', 'description', 'waf_address', 'app_address', 'total_requests', 'allowed_requests', 'blocked_requests', 'app_enabled', 'waf_enabled', 'settings', 'rules')