from django.contrib import admin
from .models import *

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'date_ordered', 'date_fulfilled', 'total_price', 'status', 'supplier', 'admin')
    inlines = [OrderProductInline]

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryOrder)
admin.site.register(Invoice)
admin.site.register(Vehicle)
admin.site.register(Reparation)
admin.site.register(ReparationProduct)
