# Generated by Django 5.1.1 on 2024-10-15 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WAF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('waf_address', models.CharField(max_length=200)),
                ('app_address', models.CharField(max_length=200)),
                ('total_requests', models.IntegerField()),
                ('allowed_requests', models.IntegerField()),
                ('blocked_requests', models.IntegerField()),
                ('app_enabled', models.BooleanField(default=False)),
                ('waf_enabled', models.BooleanField(default=False)),
                ('settings', models.JSONField(default=dict)),
                ('rules', models.JSONField(default=dict)),
            ],
        ),
    ]
