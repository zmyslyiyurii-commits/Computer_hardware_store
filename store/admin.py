from django.contrib import admin, messages
from django.utils.html import format_html_join
from store.models import Category, Order, OrderItem, Product, Review


# Налаштування керування категоріями в адмінці Django.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
    ordering = ('name',)


# Дає змогу шукати товари, фільтрувати їх і змінювати публікацію зі списку.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('stock_quantity', 'is_active')
    ordering = ('-created_at',)
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'category', 'price', 'stock_quantity', 'image_url', 'badge', 'description', 'is_active'),
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author_name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__name', 'author_name', 'text')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product_name', 'product_category', 'quantity', 'unit_price')
    readonly_fields = ('product_name', 'product_category', 'quantity', 'unit_price')
    can_delete = False

    @admin.display(description='Категорія')
    def product_category(self, obj):
        return obj.product.category.name


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'email_display', 'items_summary', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone', 'email', 'items__product_name', 'items__product__category__name')
    readonly_fields = ('customer_name', 'phone', 'email', 'delivery_address', 'total', 'created_at')
    inlines = (OrderItemInline,)
    actions = ('cancel_orders',)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.status == 'cancelled':
            return (*readonly_fields, 'status')
        return readonly_fields

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items__product__category')

    def save_model(self, request, obj, form, change):
        if change:
            previous = Order.objects.get(pk=obj.pk)
            if previous.status == 'cancelled':
                obj.status = 'cancelled'
            elif obj.status == 'cancelled' and not obj.cancel():
                obj.status = previous.status
                self.message_user(
                    request,
                    'Виконане замовлення не можна скасувати.',
                    level=messages.ERROR,
                )
        super().save_model(request, obj, form, change)

    @admin.action(description='Скасувати вибрані замовлення та повернути товари на склад')
    def cancel_orders(self, request, queryset):
        cancelled_count = 0
        skipped_count = 0
        for order in queryset:
            if order.cancel():
                cancelled_count += 1
            else:
                skipped_count += 1

        if cancelled_count:
            self.message_user(
                request,
                f'Скасовано замовлень: {cancelled_count}. Товари повернуто на склад.',
                level=messages.SUCCESS,
            )
        if skipped_count:
            self.message_user(
                request,
                f'Пропущено замовлень: {skipped_count}. Вже скасовані або виконані замовлення не змінювалися.',
                level=messages.WARNING,
            )

    @admin.display(description='Електронна пошта')
    def email_display(self, order):
        return order.email

    @admin.display(description='Склад замовлення')
    def items_summary(self, order):
        return format_html_join(
            '<br>',
            '{}',
            (
                (f'{item.product_name} — {item.product.category.name} × {item.quantity}',)
                for item in order.items.all()
            ),
        ) or 'Немає товарів'
