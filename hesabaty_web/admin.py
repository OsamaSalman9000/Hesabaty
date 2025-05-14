from django.contrib import admin
from .models import UserProfile, Building, Apartment, Tenant, Invoice, Reservation

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(Tenant)
admin.site.register(Invoice)
admin.site.register(Reservation)