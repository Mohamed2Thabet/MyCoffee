from django.contrib import admin
from .models import OrderDetails,Order
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetails)