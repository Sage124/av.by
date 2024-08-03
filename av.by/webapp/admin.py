from django.contrib import admin
from .models import *

######## Транспорт ########

#_____ Легковые авто ______
@admin.register(Car)
class CarsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "brand",
        "model",
        "year",
        "transmission",
        "body_type",
        "engine_volume",
        "color",
    ]
    search_fields = [
        "id",
        "brand",
        "model",
        "year",
        "transmission",
        "body_type",
        "engine_volume",
        "color",
    ]
