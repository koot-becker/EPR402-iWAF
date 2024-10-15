from django.db import models

class WAF(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    waf_address = models.CharField(max_length=200)
    app_address = models.CharField(max_length=200)
    total_requests = models.IntegerField()
    allowed_requests = models.IntegerField()
    blocked_requests = models.IntegerField()
    app_enabled = models.BooleanField(default=False)
    waf_enabled = models.BooleanField(default=False)
    settings = models.JSONField(default=dict)
    rules = models.JSONField(default=dict)

    def __str__(self):
        return self.name
