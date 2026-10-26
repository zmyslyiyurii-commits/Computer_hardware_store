from django.contrib import admin
from store.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'category')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
