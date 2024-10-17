from django.contrib import admin
from .models import WAF

class WAFAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'enabled')

admin.site.register(WAF)
