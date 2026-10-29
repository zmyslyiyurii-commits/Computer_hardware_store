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
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'category', 'price', 'image_url', 'badge', 'is_active'),
        }),
        ('Характеристики ноутбука для фільтрів', {
            'fields': (
                'manufacturer',
                'laptop_type',
                'display_diagonal',
                'resolution',
                'matrix_type',
                'screen_surface',
                'refresh_rate',
                'intel_generation',
                'amd_generation',
                'processor',
                'processor_cores',
                'ram_type',
                'ram_capacity',
                'ram_slots',
                'ssd_capacity',
                'graphics_type',
                'discrete_graphics_series',
                'video_memory',
                'wireless_technologies',
                'interfaces',
                'operating_system',
                'battery_capacity',
                'features',
                'weight',
                'color',
            ),
            'classes': ('collapse',),
        }),
    )
