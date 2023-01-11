"""Admin interface"""
from django.contrib import admin

from .models import Product, ScrapingTask


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product"""
    list_display = ["product_id", "title", "brand", "category", "price", ]


admin.site.register(ScrapingTask)
