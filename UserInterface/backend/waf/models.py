from django.db import models

class WAF(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    waf_address = models.CharField(max_length=200, default='')
    app_address = models.CharField(max_length=200, default='')
    waf_container_name = models.CharField(max_length=200, default='')
    app_container_name = models.CharField(max_length=200, default='')
    app_container_image_name = models.CharField(max_length=200, default='')
    app_internal_port_number = models.IntegerField(default=0)
    app_external_port_number = models.IntegerField(default=0)
    total_requests = models.IntegerField(default=0)
    average_time = models.FloatField(default=0)
    allowed_requests = models.IntegerField(default=0)
    blocked_requests = models.IntegerField(default=0)
    app_enabled = models.BooleanField(default=False)
    waf_enabled = models.BooleanField(default=False)
    settings = models.JSONField(default=dict)
    rules = models.JSONField(default=dict)
    results = models.JSONField(default=dict)

    def __str__(self):
        return self.name
