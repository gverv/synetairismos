from django.contrib import admin

# Register your models here.
# from .models import WaterConsumption, WaterCons, Persons, Counters, Paids, Fields, Receivers
from .models import Parametroi, WaterCons, Persons, Counters, Paids, Fields, Receivers


# admin.site.register(WaterConsumption)
admin.site.register(WaterCons)
admin.site.register(Persons)
admin.site.register(Counters)
admin.site.register(Paids)
admin.site.register(Fields)
admin.site.register(Receivers)
admin.site.register(Parametroi)