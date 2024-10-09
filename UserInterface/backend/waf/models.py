from django.db import models

class WAF(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    waf_address = models.CharField(max_length=200)
    web_app_address = models.CharField(max_length=200)
    total_requests = models.IntegerField()
    allowed_requests = models.IntegerField()
    blocked_requests = models.IntegerField()
    threats_detected = models.IntegerField()
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
