from django.contrib import admin
from store.models import Category, Product


# Налаштування керування категоріями в адмінці Django.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
    ordering = ('name',)


# Дає змогу шукати товари, фільтрувати їх і змінювати публікацію зі списку.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
