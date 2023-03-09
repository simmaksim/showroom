from django.contrib import admin

from .models import Car, Client, ProviderSaleHistory, Showroom, ShowroomSaleHistory

# Register your models here.
admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Showroom)
admin.site.register(ProviderSaleHistory)
admin.site.register(ShowroomSaleHistory)
