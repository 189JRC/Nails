from django.contrib import admin
from .models import Appointment, Customer, Record

admin.site.register(Appointment)
admin.site.register(Customer)
admin.site.register(Record)
