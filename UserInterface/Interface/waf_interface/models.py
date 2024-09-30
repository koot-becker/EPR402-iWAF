from django.db import models

class WebApplication(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    path = models.CharField(max_length=255)
    description = models.TextField()
    total_valid_count = models.IntegerField()
    total_anomalous_count = models.IntegerField()
    total_count = models.IntegerField()
    allowed_percentage = models.FloatField()
    denied_percentage = models.FloatField()
    true_positive_rate = models.FloatField()
    false_positive_rate = models.FloatField()
    true_negative_rate = models.FloatField()
    false_negative_rate = models.FloatField()
    accuracy = models.FloatField()