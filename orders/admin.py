from django.contrib import admin
import jmespath

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    raw_id_fields = ['product']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'order_date']
    list_filter = ['status', 'order_date']
    search_fields = ['first_name', 'address']
    inlines=[OrderItemInline]
    
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
    
