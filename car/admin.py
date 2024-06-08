from django.contrib import admin
from .models import Car, Order, Comment

admin.site.register(Car)
admin.site.register(Comment)
admin.site.register(Order)
