from django.contrib import admin

# Register your models here.
from .models import WaterConsumption, WaterCons, Customers, Counters, Paids, Fields


admin.site.register(WaterConsumption)
admin.site.register(WaterCons)
admin.site.register(Customers)
admin.site.register(Counters)
admin.site.register(Paids)
admin.site.register(Fields)
