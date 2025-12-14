from django.contrib import admin
from .models import CustomUser, Order, OrderItem
# Register your models here.

@admin.register(CustomUser)
class AdminCustomUser(admin.ModelAdmin):
    list_display=['name', 'phone']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id']

@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['id']