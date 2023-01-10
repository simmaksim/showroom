from django.contrib import admin

from .models import Car, SaleHistory, Showroom, User

# Register your models here.
admin.site.register(Car)
admin.site.register(User)
admin.site.register(Showroom)
admin.site.register(SaleHistory)
