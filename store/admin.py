from django import forms
from django.contrib import admin, messages
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.html import format_html, format_html_join
from store.models import Category, CustomerProfile, Order, OrderItem, Product, ProductImage, Review


# Налаштування керування категоріями в адмінці Django.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')


# Дає змогу шукати товари, фільтрувати їх і змінювати публікацію зі списку.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    verbose_name = 'Додаткове фото'
    verbose_name_plural = 'Галерея: додай окреме URL для кожного ракурсу'
    extra = 3
    fields = ('image_url', 'alt_text', 'position', 'preview')
    readonly_fields = ('preview',)

    @admin.display(description='Перегляд')
    def preview(self, obj):
        if not obj or not obj.image_url:
            return 'Збережи фото, щоб побачити перегляд'
        return format_html(
            '<img src="{}" alt="{}" style="width: 90px; height: 65px; object-fit: contain;">',
            obj.image_url,
            obj.alt_text or 'Фото товару',
        )


class ProductAdminForm(forms.ModelForm):
    cpu_release_date = forms.DateField(
        label='Дата виходу',
        required=False,
        input_formats=('%d.%m.%Y', '%Y-%m-%d'),
        widget=AdminDateWidget(attrs={'placeholder': 'дд.мм.рррр'}),
    )

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'category__name')
    list_editable = ('stock_quantity', 'is_active')
    inlines = (ProductImageInline,)
    ordering = ('-created_at',)
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'category', 'component_type', 'price', 'stock_quantity', 'image_url', 'badge', 'description', 'is_active'),
        }),
        ('Характеристики ноутбука', {
            'fields': (
                'manufacturer',
                'model_series',
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
                'webcam',
                'additional_features',
                'width',
                'height',
                'depth',
                'country_of_origin',
                'warranty_months',
                'features',
                'weight',
                'color',
            ),
            'classes': ('collapse',),
        }),
        ('Характеристики готового ПК', {
            'fields': (
                'computer_type',
                'computer_view',
                'computer_display_diagonal',
                'computer_screen_type',
                'computer_processor_series',
                'processor_threads',
                'computer_processor_frequency',
                'processor_boost_frequency',
                'processor_boost_supported',
                'motherboard_socket',
                'motherboard_chipset',
                'computer_graphics_type',
                'graphics_card_manufacturer',
                'computer_discrete_graphics_series',
                'computer_video_memory',
                'computer_intel_generation',
                'computer_amd_generation',
                'computer_processor',
                'computer_processor_cores',
                'computer_ram_capacity',
                'ram_form_factor',
                'computer_ram_slots',
                'computer_ram_frequency',
                'computer_ram_standard',
                'computer_ram_max_capacity',
                'computer_ram_type',
                'computer_storage_types',
                'computer_ssd_capacity',
                'computer_hdd_capacity',
                'computer_optical_drive',
                'computer_card_reader',
                'computer_built_in_microphone',
                'computer_built_in_speakers',
                'computer_audio_controller',
                'computer_multichannel_audio',
                'computer_wired_network',
                'computer_wireless_technologies',
                'computer_interfaces',
                'computer_operating_system',
                'computer_webcam',
                'computer_peripherals_included',
                'computer_additional_features',
                'computer_vesa_support',
                'computer_vr_support',
                'computer_backlit',
                'computer_features',
                'case_model',
                'case_metal_thickness',
                'case_material',
                'psu_location',
                'psu_power',
                'case_lighting',
                'cooling',
                'computer_width',
                'computer_height',
                'computer_depth',
                'computer_color',
                'computer_manufacturer',
                'computer_country_of_origin',
                'computer_warranty_months',
                'computer_weight',
            ),
            'classes': ('collapse',),
        }),
        ('Характеристики процесора', {
            'fields': (
                'cpu_manufacturer',
                'cpu_family',
                'cpu_socket',
                'cpu_core_count',
                'cpu_thread_count',
                'cpu_base_clock',
                'cpu_max_clock',
                'cpu_tdp',
                'cpu_process_technology',
                'cpu_l1_cache',
                'cpu_l2_cache',
                'cpu_l3_cache',
                'cpu_max_memory',
                'cpu_memory_type',
                'cpu_max_memory_speed',
                'cpu_memory_channels',
                'cpu_integrated_graphics',
                'cpu_intel_generation',
                'cpu_amd_architecture',
                'cpu_max_temperature',
                'cpu_unlocked_multiplier',
                'cpu_pcie_version',
                'cpu_release_date',
                'cpu_package_type',
                'cpu_cooling_included',
                'cpu_country_of_origin',
                'cpu_warranty_months',
                'cpu_barcode',
                'cpu_note',
            ),
            'classes': ('collapse',),
        }),
        ('Характеристики материнської плати', {
            'fields': (
                'motherboard_manufacturer',
                'motherboard_available_today',
                'motherboard_purpose',
                'motherboard_product_socket',
                'motherboard_supported_processors',
                'motherboard_expansion_slots',
                'motherboard_chipset_model',
                'motherboard_ram_type',
                'motherboard_ram_slots',
                'motherboard_max_ram',
                'motherboard_max_ram_frequency',
                'motherboard_ram_frequencies',
                'motherboard_dual_channel_support',
                'motherboard_ecc_support',
                'motherboard_integrated_video',
                'motherboard_audio_controller',
                'motherboard_multichannel_audio',
                'motherboard_lan_port_count',
                'motherboard_network_adapter',
                'motherboard_lan_speed',
                'motherboard_rear_ports',
                'motherboard_internal_ports',
                'motherboard_power_connector',
                'motherboard_headers',
                'motherboard_fan_headers',
                'motherboard_other_connectors',
                'motherboard_bios_type',
                'motherboard_operating_system',
                'motherboard_raid_controller',
                'motherboard_search_tag',
                'motherboard_form_factor',
                'motherboard_height',
                'motherboard_width',
                'motherboard_country_of_origin',
                'motherboard_warranty_months',
                'motherboard_barcode',
                'motherboard_note',
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
