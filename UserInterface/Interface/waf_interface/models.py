from django.db import models

class WebApplication(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    efficacy = models.FloatField()