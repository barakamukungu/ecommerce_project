from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Sum
from .models import Product, Order, OrderItem

#

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('status', 'created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
