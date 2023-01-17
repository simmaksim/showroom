from django.contrib import admin

from .models import Car, SaleHistory, Showroom, Client

# Register your models here.
admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Showroom)
admin.site.register(SaleHistory)
