from django.contrib import admin
from .models import Forecast, Region, Alert

# Register your models here.
admin.site.register(Forecast)
admin.site.register(Region)
admin.site.register(Alert)