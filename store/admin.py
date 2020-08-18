from django.contrib import admin
from .models import Product, ShippingAddress, Order, OrderItem, Customer
# Register your models here.


admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
