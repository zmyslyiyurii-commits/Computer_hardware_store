from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.admin import ProductAdmin, ProductAdminForm
from store.forms import (
    MonitorProductFilterForm,
    NetworkProductFilterForm,
    SSDProductFilterForm,
    ThermalPasteProductFilterForm,
)
from store.models import Category, Order, OrderItem, Product, ProductImage


class ProductSearchTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Ноутбуки')
        self.product = Product.objects.create(
            name='Lenovo ThinkPad X1',
            category=self.category,
            price=Decimal('42000.00'),
            model_series='ThinkPad',
        )

    def test_search_redirects_exact_category_to_category_catalog(self):
        response = self.client.get(reverse('home'), {'q': 'Ноутбуки'})

        self.assertRedirects(
            response,
            reverse('category_products', args=(self.category.pk,)),
        )

    def test_search_redirects_exact_product_to_product_page(self):
        response = self.client.get(reverse('home'), {'q': self.product.name})

        self.assertRedirects(
            response,
            reverse('product_detail', args=(self.product.pk,)),
        )

    def test_search_shows_partial_product_matches(self):
        response = self.client.get(reverse('home'), {'q': 'ThinkPad'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.product])
        self.assertContains(response, 'Результати пошуку')
        self.assertContains(response, self.product.name)

    def test_homepage_shows_only_manually_selected_popular_products(self):
        featured_component = Product.objects.create(
            name='Відеокарта для популярного блоку',
            category=Category.objects.create(name='Комплектуючі для ПК'),
            component_type='graphics_card',
            price=Decimal('10000.00'),
            is_featured=True,
        )
        featured_regular_product = Product.objects.create(
            name='Звичайний популярний товар',
            category=self.category,
            price=Decimal('12000.00'),
            is_featured=True,
        )
        Product.objects.create(
            name='Не вибраний товар',
            category=self.category,
            price=Decimal('8000.00'),
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(
            set(response.context['products']),
            {self.product, featured_component, featured_regular_product},
        )
        self.assertEqual(
            set(response.context['popular_products']),
            {featured_component, featured_regular_product},
        )
        self.assertEqual(
            set(response.context['other_products']),
            {self.product},
        )
        self.assertContains(response, 'Не вибраний товар')
        self.assertContains(response, 'Усі товари')

    def test_search_includes_products_not_selected_as_popular(self):
        response = self.client.get(reverse('home'), {'q': 'ThinkPad'})

        self.assertEqual(list(response.context['products']), [self.product])

    def test_search_matches_multiple_words_in_product_name(self):
        response = self.client.get(reverse('home'), {'q': 'Lenovo ThinkPad'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.product])

    def test_search_shows_message_when_no_products_match(self):
        response = self.client.get(reverse('home'), {'q': 'Невідомий товар'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'товарів не знайдено')

    def test_logo_on_home_page_links_to_home(self):
        response = self.client.get(reverse('home'))

        self.assertContains(
            response,
            f'<a class="logo" href="{reverse("home")}" aria-label="NEXUS — на головну">',
            html=False,
        )

    def test_product_card_can_add_and_remove_favorite_without_leaving_page(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'favorite-card-button')

        response = self.client.post(
            reverse('toggle_favorite', args=(self.product.pk,)),
            {'next_url': reverse('home')},
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['favorites'], [str(self.product.pk)])

        response = self.client.get(reverse('home'))
        self.assertContains(response, 'favorite-card-button is-favorite')

        response = self.client.post(
            reverse('toggle_favorite', args=(self.product.pk,)),
            {'next_url': reverse('home')},
        )
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.client.session['favorites'], [])

    def test_catalog_lists_pc_maintenance_instead_of_storage_category(self):
        response = self.client.get(reverse('home'))

        self.assertNotIn(
            'Аксесуари',
            [category.name for category in response.context['categories']],
        )
        self.assertTrue(Category.objects.filter(name='Обслуговування ПК').exists())
        self.assertFalse(Category.objects.filter(name='Накопичувачі').exists())
        self.assertContains(response, 'Обслуговування ПК')
        self.assertContains(response, 'Термопаста, очищення та догляд за комп’ютером')
        self.assertContains(response, 'Мережеві фільтри та подовжувачі')
        self.assertNotContains(response, 'Мережеве обладнання')
        self.assertNotContains(response, 'SSD, жорсткі диски та флешнакопичувачі')
        self.assertNotContains(response, 'Корисні доповнення до техніки')
        self.assertNotContains(response, '<strong>Аксесуари</strong>', html=False)


class ComputerComponentsCatalogTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Комплектуючі для ПК',
            icon='⚙',
        )

    def test_components_category_opens_component_picker(self):
        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
        )

        self.assertRedirects(
            response,
            reverse('computer_components', args=(self.category.pk,)),
        )

    def test_exact_category_search_opens_component_picker(self):
        response = self.client.get(
            reverse('home'),
            {'q': self.category.name},
        )

        self.assertRedirects(
            response,
            reverse('computer_components', args=(self.category.pk,)),
        )

    def test_component_picker_shows_only_pc_build_parts(self):
        response = self.client.get(
            reverse('computer_components', args=(self.category.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['component_cards']), 9)
        for title in (
            'Процесори',
            'Материнські плати',
            'Відеокарти',
            "Оперативна пам’ять",
            'SSD накопичувачі',
            'Жорсткі диски HDD',
            'Корпуси',
            'Блоки живлення',
            'Системи охолодження',
        ):
            self.assertContains(response, title)
        component_titles = {component['title'] for component in response.context['component_cards']}
        self.assertNotIn('Монітори', component_titles)
        self.assertNotIn('Маніпулятори', component_titles)
        self.assertNotIn('Обслуговування ПК', component_titles)

    def test_ssd_and_hdd_cards_link_to_separate_product_types(self):
        response = self.client.get(
            reverse('computer_components', args=(self.category.pk,)),
        )

        self.assertContains(response, '?component_type=ssd')
        self.assertContains(response, '?component_type=hdd')
        cards_by_type = {
            card['type']: card
            for card in response.context['component_cards']
        }
        self.assertEqual(
            cards_by_type['hdd']['image_url'],
            'https://brain.com.ua/static/images/prod_img/3/0/U0811330_1738963508.webp',
        )

    def test_ssd_and_hdd_catalogs_only_show_the_selected_drive_type(self):
        ssd = Product.objects.create(
            name='NVMe SSD 1TB',
            category=self.category,
            component_type='ssd',
            price=Decimal('3000.00'),
        )
        hdd = Product.objects.create(
            name='HDD 2TB',
            category=self.category,
            component_type='hdd',
            price=Decimal('2500.00'),
        )

        ssd_response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {'component_type': 'ssd'},
        )
        hdd_response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {'component_type': 'hdd'},
        )

        self.assertEqual(list(ssd_response.context['products']), [ssd])
        self.assertEqual(ssd_response.context['category_title'], 'SSD накопичувачі')
        self.assertEqual(list(hdd_response.context['products']), [hdd])
        self.assertEqual(hdd_response.context['category_title'], 'Жорсткі диски HDD')

    def test_component_picker_links_to_products_of_selected_type(self):
        processor = Product.objects.create(
            name='AMD Ryzen 5',
            category=self.category,
            component_type='processor',
            price=Decimal('5000.00'),
        )
        Product.objects.create(
            name='Материнська плата',
            category=self.category,
            component_type='motherboard',
            price=Decimal('4000.00'),
        )

        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {'component_type': 'processor'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [processor])
        self.assertEqual(response.context['category_title'], 'Процесори')
        self.assertContains(response, 'Усі комплектуючі для ПК')

    def test_home_category_card_links_to_component_picker(self):
        response = self.client.get(reverse('home'))

        self.assertContains(
            response,
            reverse('computer_components', args=(self.category.pk,)),
        )


class ProcessorCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.amd_processor = Product.objects.create(
            name='AMD Ryzen 5 7600',
            category=self.category,
            component_type='processor',
            price=Decimal('6500.00'),
            stock_quantity=3,
            cpu_manufacturer='AMD',
            cpu_family='AMD Ryzen 5',
            cpu_socket='AM5',
            cpu_core_count='6 ядер',
            cpu_thread_count='12 потоків',
            cpu_base_clock='3.8 GHz',
            cpu_max_clock='5.1 GHz',
            cpu_tdp='65 Вт',
            cpu_process_technology='7 nm',
            cpu_l1_cache='384 KB',
            cpu_l2_cache='3 MB',
            cpu_l3_cache='32 MB',
            cpu_max_memory='128 GB',
            cpu_memory_type='DDR4',
            cpu_max_memory_speed='3200 MHz',
            cpu_memory_channels='2',
            cpu_integrated_graphics='AMD Radeon Graphics',
            cpu_amd_architecture='AMD Zen 4',
            cpu_max_temperature='90°C',
            cpu_unlocked_multiplier='так',
            cpu_pcie_version='4.0',
            cpu_release_date='2022-04-04',
            cpu_package_type='BOX',
            cpu_cooling_included='кулер у комплекті',
            cpu_country_of_origin='США',
            cpu_warranty_months=36,
            cpu_barcode='5054444470061',
            cpu_note='Характеристики можуть змінюватися виробником.',
        )
        self.out_of_stock_processor = Product.objects.create(
            name='AMD Ryzen 7 7700',
            category=self.category,
            component_type='processor',
            price=Decimal('9000.00'),
            stock_quantity=0,
            cpu_manufacturer='AMD',
            cpu_family='AMD Ryzen 7',
            cpu_socket='AM5',
            cpu_core_count='8 ядер',
        )
        Product.objects.create(
            name='Intel Core i5',
            category=self.category,
            component_type='processor',
            price=Decimal('7000.00'),
            stock_quantity=2,
            cpu_manufacturer='INTEL',
            cpu_family='Intel Core i5',
            cpu_socket='1700',
            cpu_intel_generation='Alder Lake (12 покоління)',
        )
        Product.objects.create(
            name='Материнська плата',
            category=self.category,
            component_type='motherboard',
            price=Decimal('4000.00'),
            cpu_manufacturer='AMD',
            cpu_socket='AM5',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_processor_release_date_accepts_ukrainian_date_format(self):
        form = ProductAdminForm(data={
            'name': 'AMD Ryzen date test',
            'category': self.category.pk,
            'component_type': 'processor',
            'price': '5000',
            'cpu_release_date': '04.04.2022',
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data['cpu_release_date'].isoformat(),
            '2022-04-04',
        )

    def test_processor_catalog_has_own_filters_and_preserves_component_type(self):
        response = self.client.get(self.url, {'component_type': 'processor'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['processor_catalog'])
        self.assertEqual(len(response.context['filter_groups']), 13)
        self.assertNotContains(response, 'Наявність у магазині')
        self.assertContains(response, 'name="component_type" value="processor"')
        self.assertContains(response, 'AMD (2)')

    def test_processor_filters_can_be_combined(self):
        response = self.client.get(self.url, {
            'component_type': 'processor',
            'cpu_manufacturer': 'AMD',
            'cpu_socket': 'AM5',
            'cpu_amd_architecture': 'AMD Zen 4',
        })

        self.assertEqual(
            list(response.context['products']),
            [self.amd_processor],
        )

    def test_price_filter_applies_to_processors_only(self):
        response = self.client.get(self.url, {
            'component_type': 'processor',
            'price_min': '6000',
            'price_max': '6800',
        })

        self.assertEqual(list(response.context['products']), [self.amd_processor])

    def test_clear_filters_keeps_user_in_processor_catalog(self):
        response = self.client.get(self.url, {'component_type': 'processor'})

        self.assertContains(
            response,
            f'href="{self.url}?component_type=processor">Очистити',
            html=False,
        )

    def test_processor_details_show_the_processor_specific_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.amd_processor.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Сокет процесора'], 'AM5')
        self.assertEqual(specifications['Максимальний TDP процесора'], '65 Вт')
        self.assertEqual(specifications['Техпроцес'], '7 nm')
        self.assertEqual(specifications['Дата виходу'], '04.04.2022')
        self.assertEqual(specifications['Штрихкод'], '5054444470061')
        group_names = [group['name'] for group in response.context['specification_groups']]
        self.assertEqual(
            group_names,
            ['Основні технічні характеристики', "Пам'ять", 'Відео', 'Додаткові характеристики', 'Інші'],
        )


class MotherboardCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.asus_board = Product.objects.create(
            name='ASUS TUF GAMING B550M-PLUS',
            category=self.category,
            component_type='motherboard',
            price=Decimal('5499.00'),
            stock_quantity=4,
            motherboard_manufacturer='ASUS',
            motherboard_available_today=True,
            motherboard_purpose='геймерська',
            motherboard_product_socket='AM4',
            motherboard_pcie_x1_slots='2 шт',
            motherboard_pcie_x4_slots='1 шт',
            motherboard_pcie_x16_slots='2 шт',
            motherboard_pci_slots='без слота PCI',
            motherboard_chipset_model='AMD B550',
            motherboard_ram_type='DDR4',
            motherboard_ram_slots='4 шт',
            motherboard_max_ram='128 GB',
            motherboard_max_ram_frequency='4400 MHz',
            motherboard_integrated_video='З підтримкою відеоядра процесора',
            motherboard_lan_speed='2,5 Гбіт/с',
            motherboard_video_outputs='HDMI, DisplayPort',
            motherboard_usb='USB Type-C, USB 3.2',
            motherboard_digital_audio_output='оптичний',
            motherboard_m2_slots='2 шт',
            motherboard_sata3_ports='4 шт',
            motherboard_satae_slot='без SATAe інтерфейсу',
            motherboard_u2_slot='без U.2 роз’єму',
            motherboard_wireless='Bluetooth, 802.11 a/b/g/n/ac/ax',
            motherboard_raid_controller='0',
            motherboard_search_tag='материнська плата для ПК',
            motherboard_form_factor='Micro ATX',
            motherboard_supported_processors='AMD Ryzen 5000 Series Processors',
            motherboard_expansion_slots='2 x PCI-E 3.0 x1, 1 x PCI-E 3.0 x16',
            motherboard_ram_frequencies='3600 MHz, 3866 MHz, 3733 MHz',
            motherboard_dual_channel_support='так',
            motherboard_ecc_support='так',
            motherboard_audio_controller='Realtek ALC887/897',
            motherboard_multichannel_audio='7.1',
            motherboard_lan_port_count='1 шт',
            motherboard_network_adapter='Realtek GbE',
            motherboard_rear_ports='4 x USB 3.2 Gen1 Type-A, 1 x VGA, 1 x HDMI',
            motherboard_internal_ports='1 x M.2 2280, 4 x SATA 6.0 Gb/s',
            motherboard_power_connector='1 x 24-pin, 1 x 8-pin 12V',
            motherboard_headers='4 x USB 2.0, 2 x USB 3.2 Gen1',
            motherboard_fan_headers='2 шт.',
            motherboard_other_connectors='1 x COM port header, 1 x S/PDIF out header',
            motherboard_bios_type='128 Mb Flash ROM, UEFI AMI BIOS',
            motherboard_operating_system='Windows 10',
            motherboard_height='244',
            motherboard_width='244',
            motherboard_country_of_origin='Китай',
            motherboard_warranty_months=36,
            motherboard_barcode='4711081154457',
            motherboard_note='Виробник може змінювати властивості.',
        )
        self.msi_board = Product.objects.create(
            name='MSI PRO B760M',
            category=self.category,
            component_type='motherboard',
            price=Decimal('4200.00'),
            motherboard_manufacturer='MSI',
            motherboard_purpose='звичайна',
            motherboard_product_socket='1700',
            motherboard_chipset_model='Intel B760',
            motherboard_ram_type='DDR5',
            motherboard_form_factor='Micro ATX',
        )
        Product.objects.create(
            name='AMD Ryzen 5 7600',
            category=self.category,
            component_type='processor',
            price=Decimal('6500.00'),
            motherboard_manufacturer='ASUS',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_motherboard_admin_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('motherboard_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('motherboard_')
        }
        hidden_filter_fields = {
            'motherboard_pcie_x1_slots',
            'motherboard_pcie_x4_slots',
            'motherboard_pcie_x16_slots',
            'motherboard_pci_slots',
            'motherboard_video_outputs',
            'motherboard_usb',
            'motherboard_digital_audio_output',
            'motherboard_m2_slots',
            'motherboard_sata3_ports',
            'motherboard_satae_slot',
            'motherboard_u2_slot',
            'motherboard_wireless',
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields - hidden_filter_fields)

    def test_motherboard_catalog_shows_dynamic_filters_and_counts(self):
        response = self.client.get(self.url, {'component_type': 'motherboard'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.asus_board, self.msi_board])
        self.assertEqual(len(response.context['filter_groups']), 25)
        self.assertEqual(response.context['filter_form'].available_today_count, 1)
        self.assertContains(response, 'Отримати сьогодні (1)')
        self.assertContains(response, 'ASUS (1)')
        self.assertContains(response, 'AMD B550 (1)')

    def test_motherboard_filters_combine_exact_and_multi_value_fields(self):
        response = self.client.get(self.url, {
            'component_type': 'motherboard',
            'motherboard_manufacturer': 'ASUS',
            'motherboard_product_socket': 'AM4',
            'motherboard_video_outputs': 'HDMI',
            'motherboard_form_factor': 'Micro ATX',
        })

        self.assertEqual(list(response.context['products']), [self.asus_board])

    def test_motherboard_availability_and_price_filters_apply(self):
        response = self.client.get(self.url, {
            'component_type': 'motherboard',
            'available_today': 'on',
            'price_min': '5000',
        })

        self.assertEqual(list(response.context['products']), [self.asus_board])

    def test_motherboard_product_page_shows_motherboard_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.asus_board.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Сокет материнської плати'], 'AM4')
        self.assertEqual(specifications['Модель чипсета'], 'AMD B550')
        self.assertEqual(specifications['Підтримка процесорів'], 'AMD Ryzen 5000 Series Processors')
        self.assertEqual(specifications['Тип BIOS'], '128 Mb Flash ROM, UEFI AMI BIOS')
        self.assertEqual(specifications['Штрихкод'], '4711081154457')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            [
                'Основні характеристики',
                'Процесор',
                'Слоти розширення',
                'Чипсет',
                "Оперативна пам'ять",
                'Вбудована графіка',
                'Звук',
                "Провідний зв'язок",
                "Порти і роз'єми на задній панелі",
                "Внутрішні роз'єми і колодки",
                'BIOS',
                'Додатково',
                'Фізичні характеристики',
                'Інші',
            ],
        )


class LaptopSpecificationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Ноутбуки')
        self.inspiron = Product.objects.create(
            name='Dell Inspiron',
            category=self.category,
            price=Decimal('25000.00'),
            model_series='Inspiron',
            webcam='FHD 1080p',
            additional_features='Стереодинаміки',
            width='359.0',
            height='18.9',
            depth='236.5',
            country_of_origin='Китай',
            warranty_months=12,
        )
        Product.objects.create(
            name='Dell Latitude',
            category=self.category,
            price=Decimal('30000.00'),
            model_series='Latitude',
        )

    def test_new_fields_appear_in_product_specifications(self):
        response = self.client.get(reverse('product_detail', args=(self.inspiron.pk,)))

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Серія (модельний ряд)'], 'Inspiron')
        self.assertEqual(specifications['Веб-камера'], 'FHD 1080p')
        self.assertEqual(specifications['Додаткові можливості'], 'Стереодинаміки')
        self.assertEqual(specifications['Ширина, мм'], '359.0')
        self.assertEqual(specifications['Висота, мм'], '18.9')
        self.assertEqual(specifications['Глибина, мм'], '236.5')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс.'], 12)

    def test_laptop_catalog_filters_by_model_series(self):
        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {'model_series': 'Inspiron'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.inspiron])
        self.assertContains(response, 'Серія (модельний ряд)')

    def test_product_gallery_images_render_with_primary_image_first(self):
        self.inspiron.image_url = 'https://example.com/primary.jpg'
        self.inspiron.save(update_fields=['image_url'])
        ProductImage.objects.create(
            product=self.inspiron,
            image_url='https://example.com/side.jpg',
            alt_text='Вигляд збоку',
            position=1,
        )
        ProductImage.objects.create(
            product=self.inspiron,
            image_url='https://example.com/keyboard.jpg',
            alt_text='Клавіатура',
            position=2,
        )

        response = self.client.get(reverse('product_detail', args=(self.inspiron.pk,)))

        self.assertEqual(response.status_code, 200)
        images = response.context['product_images']
        self.assertEqual(
            [image['url'] for image in images],
            [
                'https://example.com/primary.jpg',
                'https://example.com/side.jpg',
                'https://example.com/keyboard.jpg',
            ],
        )
        self.assertContains(response, 'data-gallery-thumb', count=3)


class ComputerSpecificationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комп’ютери')
        self.computer = Product.objects.create(
            name='Vinga Rhino D9079',
            category=self.category,
            price=Decimal('41557.00'),
            computer_type='Ігрові',
            computer_view='Класичні',
            computer_processor_series='AMD Ryzen 5',
            computer_amd_generation='Zen 3',
            computer_processor='AMD Ryzen 5 5500',
            computer_processor_cores='6 ядер',
            processor_threads='12 потоків',
            computer_processor_frequency='3.6 ГГц',
            processor_boost_frequency='4.2',
            processor_boost_supported='Є',
            motherboard_socket='AM4',
            motherboard_chipset='AMD A520',
            computer_graphics_type='Дискретна',
            graphics_card_manufacturer='NVIDIA',
            computer_discrete_graphics_series='GeForce RTX 3050',
            computer_video_memory='6 ГБ',
            computer_ram_capacity='16 ГБ',
            ram_form_factor='DIMM',
            computer_ram_type='DDR4',
            computer_ram_frequency='3200 МГц',
            computer_ram_standard='PC4-25600',
            computer_ram_max_capacity='64 ГБ',
            computer_storage_types='SSD',
            computer_ssd_capacity='512 ГБ',
            computer_hdd_capacity='Немає',
            computer_optical_drive='Немає',
            computer_card_reader='Немає',
            computer_built_in_microphone='Немає',
            computer_webcam='Немає',
            computer_built_in_speakers='Немає',
            computer_audio_controller='Realtek',
            computer_multichannel_audio='7.1',
            computer_wired_network='10/100/1000 Мбіт/с',
            computer_interfaces='USB, HDMI, DisplayPort',
            computer_operating_system='Без ОС',
            computer_peripherals_included='Немає',
            computer_additional_features='Контролер підсвічування',
            computer_vesa_support='Немає',
            computer_vr_support='Є',
            computer_backlit='Є',
            case_model='Vinga Cello',
            case_metal_thickness='0.75 мм',
            case_material='Скло, пластик, метал',
            psu_location='Нижнє',
            psu_power='600 Вт',
            case_lighting='ARGB',
            cooling='4 вентилятори з підсвічуванням',
            computer_width='225',
            computer_height='450',
            computer_depth='390',
            computer_manufacturer='Vinga',
            computer_country_of_origin='Україна',
            computer_warranty_months=36,
        )

    def test_computer_details_show_specs_in_reference_groups(self):
        response = self.client.get(
            reverse('product_detail', args=(self.computer.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        group_names = [
            group['name']
            for group in response.context['specification_groups']
        ]
        self.assertEqual(
            group_names,
            [
                'Основні характеристики',
                'Процесор',
                'Материнська плата',
                'Відеокарта',
                "Оперативна пам'ять",
                'Система зберігання',
                'Мультимедіа',
                'Комунікаційні можливості',
                'Порти та роз’єми',
                'Програмне забезпечення',
                'Додатково',
                'Корпус',
                'Інші характеристики',
            ],
        )
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Тип ПК'], 'Ігрові')
        self.assertEqual(specifications['Кількість потоків'], '12 потоків')
        self.assertEqual(specifications['Сокет'], 'AM4')
        self.assertEqual(specifications['Потужність блоку живлення'], '600 Вт')
        self.assertEqual(specifications['Гарантія, міс.'], 36)

    def test_computer_catalog_has_reference_filters_and_filters_products(self):
        office_computer = Product.objects.create(
            name='Офісний ПК',
            category=self.category,
            price=Decimal('20000.00'),
            computer_type='Для роботи та навчання',
            computer_manufacturer='Other',
        )

        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {'computer_type': 'Ігрові'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.computer])
        self.assertContains(response, 'Виробник')
        self.assertContains(response, 'Тип ПК')
        self.assertContains(response, 'Діагональ екрану')
        self.assertContains(response, 'Серія процесора')
        self.assertContains(response, 'Модель відеокарти')
        self.assertContains(response, 'З підтримкою VR')
        self.assertNotContains(response, office_computer.name)

    def test_computer_catalog_combines_filters_and_supports_frequency_ranges(self):
        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {
                'computer_manufacturer': 'Vinga',
                'computer_processor_frequency': 'понад 3.5 ГГц',
                'computer_ram_capacity': '16 ГБ',
                'computer_ssd_capacity': '512 ГБ',
                'computer_interfaces': 'HDMI',
                'computer_vr_support': 'Є',
                'computer_backlit': 'Є',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.computer])

    def test_computer_binary_filters_merge_case_and_absence_variants(self):
        computer_without_dvd = Product.objects.create(
            name='ПК без DVD',
            category=self.category,
            price=Decimal('30000.00'),
            computer_optical_drive='без DVD',
        )

        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
            {'computer_optical_drive': 'Немає'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context['products'],
            [self.computer, computer_without_dvd],
        )
        optical_drive_choices = dict(
            response.context['filter_form'].fields['computer_optical_drive'].choices
        )
        self.assertEqual(optical_drive_choices['Немає'], 'Немає (2)')
        self.assertNotIn('немає', optical_drive_choices)
        self.assertNotIn('без DVD', optical_drive_choices)

    def test_computer_category_catalog_shows_its_products(self):
        response = self.client.get(
            reverse('category_products', args=(self.category.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.computer])
        self.assertContains(response, self.computer.name)

    def test_pc_specs_are_not_used_for_pc_components_category(self):
        components_category = Category.objects.create(name='Комплектуючі для ПК')
        components_product = Product.objects.create(
            name='Відеокарта',
            category=components_category,
            price=Decimal('10000.00'),
            computer_processor='Не характеристика відеокарти',
        )

        response = self.client.get(
            reverse('product_detail', args=(components_product.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Характеристики готового ПК')
        self.assertNotContains(response, 'Не характеристика відеокарти')


class CustomerAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer',
            password='test-password-123',
            first_name='Олена',
            last_name='Покупець',
            email='olena@example.com',
        )
        self.client.force_login(self.user)

    def test_profile_shows_order_history_and_favorite_link(self):
        category = Category.objects.create(name='Ноутбуки')
        product = Product.objects.create(
            name='Мій ноутбук',
            category=category,
            price=Decimal('100.00'),
            stock_quantity=1,
        )
        order = self.user.store_orders.create(
            customer_name='Олена Покупець',
            phone='+380501234567',
            email='olena@example.com',
            delivery_address='Київ',
            total=Decimal('100.00'),
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            quantity=1,
            unit_price=product.price,
        )

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мій ноутбук')
        self.assertContains(response, 'Обране')
        self.assertContains(response, 'Персональні дані')

    def test_profile_sidebar_switches_between_sections(self):
        favorites_response = self.client.get(
            reverse('profile'),
            {'section': 'favorites'},
        )
        personal_response = self.client.get(
            reverse('profile'),
            {'section': 'personal'},
        )

        self.assertContains(favorites_response, 'Обране поки порожнє')
        self.assertNotContains(favorites_response, 'Мої замовлення</h1>')
        self.assertContains(personal_response, 'Зберегти зміни')
        self.assertNotContains(personal_response, 'Обране поки порожнє')

    def test_profile_personal_data_can_be_updated(self):
        response = self.client.post(
            reverse('profile'),
            {
                'first_name': 'Ірина',
                'last_name': 'Клієнтка',
                'email': 'iryna@example.com',
                'phone': '+380671112233',
            },
        )

        self.assertRedirects(
            response,
            f'{reverse("profile")}?section=personal#personal-data',
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Ірина')
        self.assertEqual(self.user.email, 'iryna@example.com')
        self.assertEqual(self.user.customer_profile.phone, '+380671112233')

    def test_new_checkout_order_is_linked_to_logged_in_account(self):
        category = Category.objects.create(name='Ноутбуки')
        product = Product.objects.create(
            name='Ноутбук для замовлення',
            category=category,
            price=Decimal('100.00'),
            stock_quantity=1,
        )
        session = self.client.session
        session['cart'] = {str(product.pk): 1}
        session.save()

        response = self.client.post(
            reverse('checkout'),
            {
                'customer_name': 'Олена Покупець',
                'phone': '+380501234567',
                'email': 'olena@example.com',
                'delivery_address': 'Київ',
            },
        )

        self.assertRedirects(response, reverse('order_success'))
        self.assertEqual(Order.objects.get().user, self.user)


class VideoCardCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.asus_card = Product.objects.create(
            name='ASUS GeForce RTX 5060',
            category=self.category,
            component_type='graphics_card',
            price=Decimal('18000.00'),
            video_card_manufacturer='ASUS',
            video_card_family='NVIDIA',
            video_card_form_factor='стандартна',
            video_card_purpose='ігрова',
            video_card_chip='GeForce RTX 5060',
            video_card_interface='PCI-Express 5.0',
            video_card_memory_capacity='8 ГБ',
            video_card_memory_type='GDDR7',
            video_card_memory_bus='128 Bit',
            video_card_connectors='2 x HDMI, 1 x DisplayPort',
            video_card_cooling_system='активний',
            video_card_cooling_type='кулер',
            video_card_fan_count='2 шт',
            video_card_power_connectors='8 pin',
            video_card_boost_clock='2647 MHz',
            video_card_memory_frequency='28000 MHz',
            video_card_max_displays='4',
            video_card_max_resolution='7680 x 4320',
            video_card_hdcp='так',
            video_card_recommended_psu='600 Вт',
            video_card_directx='12 Ultimate',
            video_card_opengl='4.6',
            video_card_dlss='DLSS 4',
            video_card_dimensions='300 x 125 x 44 мм',
            video_card_weight='838 г',
            video_card_country_of_origin='Китай',
            video_card_warranty_months=36,
            video_card_barcode='4711377341394',
            video_card_note='Виробник може змінювати властивості.',
        )
        self.msi_card = Product.objects.create(
            name='MSI Radeon RX 580',
            category=self.category,
            component_type='graphics_card',
            price=Decimal('7000.00'),
            video_card_manufacturer='MSI',
            video_card_family='AMD',
            video_card_chip='Radeon RX 580',
            video_card_connectors='1 x DVI, 1 x VGA',
            video_card_memory_capacity='8 ГБ',
        )
        Product.objects.create(
            name='ASUS материнська плата',
            category=self.category,
            component_type='motherboard',
            price=Decimal('5000.00'),
            video_card_manufacturer='ASUS',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_video_card_catalog_has_dynamic_filter_values_and_counts(self):
        response = self.client.get(self.url, {'component_type': 'graphics_card'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['video_card_catalog'])
        self.assertEqual(list(response.context['products']), [self.asus_card, self.msi_card])
        self.assertEqual(len(response.context['filter_groups']), 14)
        self.assertContains(response, 'ASUS (1)')
        self.assertContains(response, 'HDMI (1)')
        self.assertContains(response, 'DisplayPort (1)')
        self.assertContains(response, 'VGA (D-Sub) (1)')
        self.assertNotContains(response, 'HP (1)')

    def test_video_card_filters_combine_exact_and_connector_matches(self):
        response = self.client.get(self.url, {
            'component_type': 'graphics_card',
            'video_card_manufacturer': 'ASUS',
            'video_card_chip': 'GeForce RTX 5060',
            'video_card_connectors': 'HDMI',
            'video_card_memory_type': 'GDDR7',
        })

        self.assertEqual(list(response.context['products']), [self.asus_card])

    def test_video_card_connector_filter_matches_counted_vga_names(self):
        response = self.client.get(self.url, {
            'component_type': 'graphics_card',
            'video_card_connectors': 'VGA (D-Sub)',
        })

        self.assertEqual(list(response.context['products']), [self.msi_card])

    def test_video_card_price_and_component_type_filters_are_scoped(self):
        response = self.client.get(self.url, {
            'component_type': 'graphics_card',
            'price_min': '6500',
            'price_max': '8000',
        })

        self.assertEqual(list(response.context['products']), [self.msi_card])

    def test_video_card_admin_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('video_card_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('video_card_')
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_video_card_product_page_shows_video_card_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.asus_card.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Графічний чип'], 'GeForce RTX 5060')
        self.assertEqual(specifications['Об’єм вбудованої пам’яті'], '8 ГБ')
        self.assertEqual(specifications['Роз’єми відеокарти'], '2 x HDMI, 1 x DisplayPort')
        self.assertEqual(specifications['Частота ядра (Boost)'], '2647 MHz')
        self.assertEqual(specifications['Виробник'], 'ASUS')
        self.assertEqual(specifications['Штрихкод'], '4711377341394')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики'],
        )


class MemoryCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.kingston_memory = Product.objects.create(
            name='Kingston Fury DDR5 32GB',
            category=self.category,
            component_type='memory',
            price=Decimal('4500.00'),
            memory_purpose='для ПК',
            memory_manufacturer='Kingston',
            memory_type='DDR5',
            memory_capacity='32 ГБ',
            memory_frequency='5600 МГц',
            memory_module_count='2',
            memory_timing='CL36',
            memory_voltage='1.25 В',
            memory_cooling='радіатор',
            memory_lighting='є',
            memory_overclock_profiles='EXPO, XMP',
            memory_standard='PC5-44800',
            memory_form_factor='288-pin DIMM',
            memory_ecc='ні',
            memory_buffering='unbuffered',
            memory_additional_note='Поставка можлива в OEM-версії.',
            memory_country_of_origin='Тайвань',
            memory_warranty_months=99,
            memory_barcode='740617319903',
            memory_note='Виробник може змінювати властивості.',
        )
        self.samsung_memory = Product.objects.create(
            name='Samsung DDR4 16GB',
            category=self.category,
            component_type='memory',
            price=Decimal('1800.00'),
            memory_purpose='для ноутбуків',
            memory_manufacturer='Samsung',
            memory_type='DDR4',
            memory_capacity='16 ГБ',
            memory_frequency='3200 МГц',
            memory_module_count='1',
            memory_timing='CL22',
            memory_voltage='1.2 В',
            memory_cooling='немає',
            memory_lighting='немає',
        )
        Product.objects.create(
            name='Процесор AMD Ryzen',
            category=self.category,
            component_type='processor',
            price=Decimal('6000.00'),
            memory_manufacturer='Kingston',
            memory_type='DDR5',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_memory_catalog_displays_filter_groups_and_dynamic_counts(self):
        response = self.client.get(self.url, {'component_type': 'memory'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['memory_catalog'])
        self.assertEqual(
            list(response.context['products']),
            [self.kingston_memory, self.samsung_memory],
        )
        self.assertEqual(len(response.context['filter_groups']), 11)
        self.assertContains(response, 'Kingston (1)')
        self.assertContains(response, 'DDR5 (1)')
        self.assertContains(response, 'EXPO (1)')
        self.assertContains(response, 'XMP (1)')

    def test_memory_filters_combine_exact_and_multi_value_fields(self):
        response = self.client.get(self.url, {
            'component_type': 'memory',
            'memory_manufacturer': 'Kingston',
            'memory_type': 'DDR5',
            'memory_capacity': '32 ГБ',
            'memory_overclock_profiles': 'EXPO',
        })

        self.assertEqual(list(response.context['products']), [self.kingston_memory])

    def test_memory_price_filter_is_scoped_to_memory_products(self):
        response = self.client.get(self.url, {
            'component_type': 'memory',
            'price_min': '2000',
        })

        self.assertEqual(list(response.context['products']), [self.kingston_memory])

    def test_memory_admin_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('memory_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('memory_')
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_memory_product_page_shows_memory_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.kingston_memory.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Тип пам’яті'], 'DDR5')
        self.assertEqual(specifications['Об’єм пам’яті'], '32 ГБ')
        self.assertEqual(specifications['Кількість модулів у наборі'], '2')
        self.assertEqual(specifications['Стандарти пам’яті'], 'PC5-44800')
        self.assertEqual(specifications['Таймінги'], 'CL36')
        self.assertEqual(specifications['Форм-фактор пам’яті'], '288-pin DIMM')
        self.assertEqual(specifications['Країна виробництва'], 'Тайвань')
        self.assertEqual(specifications['Штрихкод'], '740617319903')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики', 'Додатково', 'Інші'],
        )


class SSDCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.nvme_ssd = Product.objects.create(
            name='Kingston NV2 1TB',
            category=self.category,
            component_type='ssd',
            price=Decimal('2800.00'),
            model_series='NV2',
            ssd_manufacturer='Kingston',
            ssd_drive_type='внутрішній',
            ssd_component_capacity='1 TB',
            ssd_flash_type='3D NAND',
            ssd_form_factor='M.2',
            ssd_m2_size='M.2 2280',
            ssd_interface='PCI Express 4.0 x4',
            ssd_read_speed='3500 MB/s',
            ssd_write_speed='2100 MB/s',
            ssd_thickness='2.2 мм',
            ssd_endurance='1.5 млн годин',
            ssd_tbw='600',
            ssd_power_consumption='7.6 Вт',
            ssd_dimensions='80 x 22 x 2.2 мм',
            ssd_weight='9 г',
            ssd_color='чорний',
            ssd_country_of_origin='Тайвань',
            ssd_warranty_months=60,
            ssd_barcode='8806095811628',
            ssd_note='Характеристики можуть змінюватися виробником.',
        )
        self.external_ssd = Product.objects.create(
            name='Portable SSD 512GB',
            category=self.category,
            component_type='ssd',
            price=Decimal('2200.00'),
            ssd_manufacturer='Samsung',
            ssd_drive_type='зовнішній',
            ssd_component_capacity='512 GB',
            ssd_flash_type='TLC',
            ssd_form_factor='portable',
            ssd_interface='USB Type-C',
            ssd_read_speed='500 MB/s',
            ssd_write_speed='450 MB/s',
            ssd_thickness='7 мм',
        )
        Product.objects.create(
            name='HDD 2TB',
            category=self.category,
            component_type='hdd',
            price=Decimal('2500.00'),
            ssd_manufacturer='Kingston',
            ssd_read_speed='3500 MB/s',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_ssd_catalog_shows_filter_options_and_counts(self):
        response = self.client.get(self.url, {'component_type': 'ssd'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['ssd_catalog'])
        self.assertEqual(list(response.context['products']), [self.nvme_ssd, self.external_ssd])
        self.assertEqual(len(response.context['filter_groups']), 10)
        self.assertContains(response, 'Kingston (1)')
        self.assertContains(response, '1 TB (1)')
        self.assertContains(response, '3001-4000Mb/s (1)')
        self.assertContains(response, '401-500Mb/s (1)')

    def test_ssd_filters_can_be_combined_and_speed_uses_ranges(self):
        response = self.client.get(self.url, {
            'component_type': 'ssd',
            'ssd_manufacturer': 'Kingston',
            'ssd_form_factor': 'M.2',
            'ssd_interface': 'PCI Express 4.0 x4',
            'ssd_read_speed': '3001-4000Mb/s',
            'ssd_write_speed': '2001-3000Mb/s',
        })

        self.assertEqual(list(response.context['products']), [self.nvme_ssd])

    def test_ssd_speed_parser_normalizes_gigabytes_per_second(self):
        self.assertEqual(SSDProductFilterForm.parse_speed('7 GB/s'), Decimal('7000'))

    def test_ssd_price_filter_does_not_include_hdd_products(self):
        response = self.client.get(self.url, {
            'component_type': 'ssd',
            'price_min': '2000',
            'price_max': '3000',
        })

        self.assertEqual(list(response.context['products']), [self.nvme_ssd, self.external_ssd])

    def test_ssd_admin_filter_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('ssd_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('ssd_')
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_ssd_product_page_shows_ssd_specifications_and_only_related_ssds(self):
        response = self.client.get(
            reverse('product_detail', args=(self.nvme_ssd.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Тип накопичувача'], 'внутрішній')
        self.assertEqual(specifications['Серія (модельний ряд)'], 'NV2')
        self.assertEqual(specifications['Об’єм SSD накопичувача'], '1 TB')
        self.assertEqual(specifications['Швидкість читання SSD'], '3500 MB/s')
        self.assertEqual(specifications['Напрацювання на відмову SSD'], '1.5 млн годин')
        self.assertEqual(specifications['TBW SSD'], '600')
        self.assertEqual(specifications['Габарити SSD'], '80 x 22 x 2.2 мм')
        self.assertEqual(specifications['Країна виробництва SSD'], 'Тайвань')
        self.assertEqual(specifications['Гарантія SSD, міс.'], 60)
        self.assertEqual(specifications['Штрихкод SSD'], '8806095811628')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики', 'Додатково', 'Фізичні характеристики', 'Інші'],
        )
        self.assertEqual(list(response.context['related_products']), [self.external_ssd])

    def test_ssd_product_page_falls_back_to_legacy_capacity_field(self):
        legacy_capacity_ssd = Product.objects.create(
            name='Legacy capacity SSD',
            category=self.category,
            component_type='ssd',
            price=Decimal('1900.00'),
            ssd_capacity='256 GB',
        )

        response = self.client.get(
            reverse('product_detail', args=(legacy_capacity_ssd.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Об’єм SSD накопичувача'], '256 GB')


class HDDCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.desktop_hdd = Product.objects.create(
            name='Seagate IronWolf 4TB',
            category=self.category,
            component_type='hdd',
            price=Decimal('4800.00'),
            hdd_drive_type='для ПК',
            hdd_manufacturer='Seagate',
            hdd_component_capacity='4 TB',
            hdd_form_factor='3.5"',
            hdd_rpm='7200 об/хв',
            hdd_buffer_size='256 MB',
            hdd_interface='SATA III',
            hdd_series='IronWolf',
            hdd_country_of_origin='Таїланд',
            hdd_warranty_months=24,
            hdd_barcode='718037782881',
            hdd_note='Характеристики можуть змінюватися виробником.',
        )
        self.laptop_hdd = Product.objects.create(
            name='Toshiba L200 1TB',
            category=self.category,
            component_type='hdd',
            price=Decimal('2200.00'),
            hdd_drive_type='для ноутбука',
            hdd_manufacturer='Toshiba',
            hdd_component_capacity='1 TB',
            hdd_form_factor='2.5"',
            hdd_rpm='5400 об/хв',
            hdd_buffer_size='128 MB',
            hdd_interface='SATA III',
        )
        Product.objects.create(
            name='SSD excluded from HDD filters',
            category=self.category,
            component_type='ssd',
            price=Decimal('3000.00'),
            hdd_manufacturer='Seagate',
            hdd_component_capacity='4 TB',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_hdd_catalog_shows_filter_groups_and_dynamic_counts(self):
        response = self.client.get(self.url, {'component_type': 'hdd'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['hdd_catalog'])
        self.assertEqual(
            list(response.context['products']),
            [self.laptop_hdd, self.desktop_hdd],
        )
        self.assertEqual(len(response.context['filter_groups']), 7)
        self.assertContains(response, 'для ПК (1)')
        self.assertContains(response, 'Seagate (1)')
        self.assertContains(response, '4 TB (1)')
        self.assertContains(response, '3.5" (1)')
        self.assertContains(response, '7200 об/хв (1)')
        self.assertContains(response, '256 MB (1)')
        self.assertContains(response, 'SATA III (2)')

    def test_hdd_filters_can_be_combined_and_remain_scoped_to_hdd(self):
        response = self.client.get(self.url, {
            'component_type': 'hdd',
            'hdd_drive_type': 'для ПК',
            'hdd_manufacturer': 'Seagate',
            'hdd_component_capacity': '4 TB',
            'hdd_form_factor': '3.5"',
            'hdd_rpm': '7200 об/хв',
            'hdd_buffer_size': '256 MB',
            'hdd_interface': 'SATA III',
        })

        self.assertEqual(list(response.context['products']), [self.desktop_hdd])

    def test_hdd_price_filter_only_filters_hdd_catalog(self):
        response = self.client.get(self.url, {
            'component_type': 'hdd',
            'price_max': '3000',
        })

        self.assertEqual(list(response.context['products']), [self.laptop_hdd])

    def test_hdd_admin_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('hdd_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('hdd_') and field.name != 'hdd_capacity'
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_hdd_product_page_shows_grouped_hdd_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.desktop_hdd.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Об’єм'], '4 TB')
        self.assertEqual(specifications['Швидкість обертання шпинделя'], '7200 об/хв')
        self.assertEqual(specifications['Розмір буфера'], '256 MB')
        self.assertEqual(specifications['Інтерфейс'], 'SATA III')
        self.assertEqual(specifications['Форм-фактор'], '3.5"')
        self.assertEqual(specifications['Лінійка (Серія)'], 'IronWolf')
        self.assertEqual(specifications['Виробник'], 'Seagate')
        self.assertEqual(specifications['Країна виробництва'], 'Таїланд')
        self.assertEqual(specifications['Гарантія, міс'], 24)
        self.assertEqual(specifications['Штрихкод'], '718037782881')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики', 'Інші'],
        )

    def test_hdd_product_page_uses_legacy_shared_fields_when_specific_fields_are_empty(self):
        legacy_hdd = Product.objects.create(
            name='Legacy HDD',
            category=self.category,
            component_type='hdd',
            price=Decimal('1800.00'),
            manufacturer='WD',
            hdd_capacity='500 GB',
            model_series='WD Blue',
            country_of_origin='Таїланд',
            warranty_months=24,
            features='Виробник може змінювати властивості.',
        )

        response = self.client.get(
            reverse('product_detail', args=(legacy_hdd.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Об’єм'], '500 GB')
        self.assertEqual(specifications['Виробник'], 'WD')
        self.assertEqual(specifications['Лінійка (Серія)'], 'WD Blue')
        self.assertEqual(specifications['Країна виробництва'], 'Таїланд')
        self.assertEqual(specifications['Гарантія, міс'], 24)
        self.assertEqual(
            specifications['Примітка'],
            'Виробник може змінювати властивості.',
        )


class ComputerCaseCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.gaming_case = Product.objects.create(
            name='MONTECH AIR 903 MAX',
            category=self.category,
            component_type='case',
            price=Decimal('3500.00'),
            case_manufacturer='MONTECH',
            case_class='Геймерські',
            case_form_factor='Miditower',
            case_installation='вертикальний',
            case_supported_motherboards='ATX, micro-ATX, Mini-ITX',
            case_psu_included='без блоку живлення',
            psu_location='нижнє',
            psu_power='750 Вт',
            case_3_5_bays='2',
            case_fan_configuration='3 x 120 мм, 1 x 140 мм',
            case_external_connectors='USB 2.0, USB 3.0, Audio',
            case_color='чорний',
            case_external_bays_5_25='відсутній',
            case_external_bays_3_5='відсутній',
            case_internal_bays_5_25='відсутній',
            case_internal_bays_2_5='2',
            case_expansion_slots='4',
            case_additional_fan_positions='Top 3x12 or 2x14 см',
            case_cooling_elements='вентиляційні решітки',
            case_dust_filter='так',
            case_liquid_cooling_support='так',
            case_max_noise='33 дБ',
            case_gpu_clearance='420 мм',
            case_cpu_cooler_clearance='175 мм',
            case_dimensions='441 x 236 x 460 мм',
            case_weight='9',
            case_barcode='4711636006521',
            case_country_of_origin='Китай',
            case_warranty_months=36,
            case_note='Виробник може змінювати властивості.',
            case_lighting='ARGB-підсвічування',
            case_material='скло, сталь, пластик',
            computer_additional_features='з безгвинтовим кріпленням',
        )
        self.compact_case = Product.objects.create(
            name='2E Minitower',
            category=self.category,
            component_type='case',
            price=Decimal('2400.00'),
            case_manufacturer='2E',
            case_class='Класичні',
            case_form_factor='Minitower',
            case_installation='вертикальний',
            case_supported_motherboards='micro-ATX, Mini-ITX',
            case_psu_included='з блоком живлення',
            psu_location='верхнє',
            psu_power='500 Вт',
            case_3_5_bays='1',
            case_fan_configuration='1 x 120 мм',
            case_external_connectors='USB 2.0, Audio',
            case_color='білий',
        )
        Product.objects.create(
            name='SSD excluded from case filters',
            category=self.category,
            component_type='ssd',
            price=Decimal('3000.00'),
            case_manufacturer='MONTECH',
            case_class='Геймерські',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_case_catalog_shows_dynamic_filter_groups_and_counts(self):
        response = self.client.get(self.url, {'component_type': 'case'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['case_catalog'])
        self.assertEqual(
            list(response.context['products']),
            [self.compact_case, self.gaming_case],
        )
        self.assertEqual(len(response.context['filter_groups']), 12)
        self.assertContains(response, 'MONTECH (1)')
        self.assertContains(response, 'Геймерські (1)')
        self.assertContains(response, 'Miditower (1)')
        self.assertContains(response, 'ATX (1)')
        self.assertContains(response, 'USB 3.0 (1)')
        self.assertContains(response, 'чорний (1)')

    def test_case_filters_combine_exact_and_multi_value_characteristics(self):
        response = self.client.get(self.url, {
            'component_type': 'case',
            'case_manufacturer': 'MONTECH',
            'case_class': 'Геймерські',
            'case_form_factor': 'Miditower',
            'case_installation': 'вертикальний',
            'case_supported_motherboards': 'ATX',
            'case_psu_included': 'без блоку живлення',
            'psu_location': 'нижнє',
            'psu_power': '750 Вт',
            'case_3_5_bays': '2',
            'case_fan_configuration': '3 x 120 мм',
            'case_external_connectors': 'USB 3.0',
            'case_color': 'чорний',
        })

        self.assertEqual(list(response.context['products']), [self.gaming_case])

    def test_case_price_filter_is_scoped_to_case_catalog(self):
        response = self.client.get(self.url, {
            'component_type': 'case',
            'price_max': '3000',
        })

        self.assertEqual(list(response.context['products']), [self.compact_case])

    def test_case_filter_fields_are_unique_and_present_in_admin(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('case_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('case_')
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_case_product_page_shows_full_case_specification_groups(self):
        response = self.client.get(
            reverse('product_detail', args=(self.gaming_case.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Клас корпусу'], 'Геймерські')
        self.assertEqual(specifications['Типорозмір'], 'Miditower')
        self.assertEqual(specifications['Розташування блоку живлення'], 'нижнє')
        self.assertEqual(specifications['Кількість зовнішніх відсіків 5.25"'], 'відсутній')
        self.assertEqual(specifications['Кількість внутрішніх відсіків 2.5"'], '2')
        self.assertEqual(specifications['Кількість слотів розширення'], '4')
        self.assertEqual(specifications['Кількість і розмір встановлених вентиляторів'], '3 x 120 мм, 1 x 140 мм')
        self.assertEqual(specifications['Пиловий фільтр'], 'так')
        self.assertEqual(specifications['Зовнішні роз’єми'], 'USB 2.0, USB 3.0, Audio')
        self.assertEqual(specifications['Встановлення довгих відеокарт'], '420 мм')
        self.assertEqual(specifications['Розмір, мм'], '441 x 236 x 460 мм')
        self.assertEqual(specifications['Виробник'], 'MONTECH')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс'], 36)
        self.assertEqual(specifications['Штрихкод'], '4711636006521')
        self.assertEqual(specifications['Примітка'], 'Виробник може змінювати властивості.')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            [
                'Основні характеристики',
                'Зовнішні відсіки',
                'Внутрішні відсіки',
                'Слоти розширення',
                'Охолодження',
                'Функції та можливості',
                'Фізичні характеристики',
                'Інші',
            ],
        )


class PowerSupplyCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.modular_gold_psu = Product.objects.create(
            name='Seasonic Focus GX-750',
            category=self.category,
            component_type='power_supply',
            price=Decimal('5200.00'),
            psu_manufacturer='Seasonic',
            psu_type="для комп'ютерів",
            psu_standard='ATX (PS/2)',
            psu_wattage='750 Вт',
            psu_modular_connection='Full',
            psu_certification='80 PLUS Gold',
            psu_pfc='активний',
            psu_pcie_connectors='4',
            psu_sata_connectors='6',
            psu_fan_diameter='120 мм',
            psu_motherboard_connector='20+4 pin',
            psu_cpu_connector='2x4+4 pin',
            psu_gpu_connector='4x6+2 pin',
            psu_peripheral_connectors='3',
            psu_output_current_5v='18A',
            psu_output_current_3_3v='18A',
            psu_output_current_12v='58A',
            psu_output_current_minus_12v='0.3A',
            psu_output_current_5vsb='3A',
            psu_cooling_type='вентилятор',
            psu_protection='OPP, SCP, UVP, OVP',
            psu_dimensions='140 x 150 x 86 мм',
            psu_country_of_origin='Китай',
            psu_warranty_months=12,
            psu_barcode='4823093320123',
            country_of_origin='Китай',
            warranty_months=12,
            features='Виробник може змінювати властивості.',
        )
        self.server_psu = Product.objects.create(
            name='FSP Server 1200',
            category=self.category,
            component_type='power_supply',
            price=Decimal('8900.00'),
            psu_manufacturer='FSP',
            psu_type='для серверних корпусів',
            psu_standard='ATX (PS/2)',
            psu_wattage='1200 Вт',
            psu_modular_connection='не має',
            psu_certification='80 PLUS Platinum',
            psu_pfc='активний',
            psu_pcie_connectors='2',
            psu_sata_connectors='3',
            psu_fan_diameter='80 мм',
        )
        Product.objects.create(
            name='Case to exclude from PSU filters',
            category=self.category,
            component_type='case',
            price=Decimal('4000.00'),
            psu_manufacturer='Seasonic',
            psu_type="для комп'ютерів",
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_power_supply_catalog_shows_dynamic_filter_groups_and_sata_ranges(self):
        response = self.client.get(self.url, {'component_type': 'power_supply'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['power_supply_catalog'])
        self.assertEqual(
            list(response.context['products']),
            [self.server_psu, self.modular_gold_psu],
        )
        self.assertEqual(len(response.context['filter_groups']), 10)
        self.assertContains(response, 'Seasonic (1)')
        self.assertContains(response, '80 PLUS Gold (1)')
        self.assertContains(response, '750 Вт (1)')
        self.assertContains(response, '3 і менше (1)')
        self.assertContains(response, '6 - 7 (1)')
        self.assertContains(response, '120 мм (1)')

    def test_power_supply_filters_combine_exact_values_and_sata_ranges(self):
        response = self.client.get(self.url, {
            'component_type': 'power_supply',
            'psu_manufacturer': 'Seasonic',
            'psu_type': "для комп'ютерів",
            'psu_standard': 'ATX (PS/2)',
            'psu_wattage': '750 Вт',
            'psu_modular_connection': 'Full',
            'psu_certification': '80 PLUS Gold',
            'psu_pfc': 'активний',
            'psu_pcie_connectors': '4',
            'psu_sata_connectors': '6 - 7',
            'psu_fan_diameter': '120 мм',
        })

        self.assertEqual(list(response.context['products']), [self.modular_gold_psu])

    def test_power_supply_admin_fields_are_unique_and_present(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('psu_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('psu_')
        }

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_power_supply_product_page_shows_detailed_reference_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.modular_gold_psu.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Тип БЖ'], "для комп'ютерів")
        self.assertEqual(specifications['Потужність'], '750 Вт')
        self.assertEqual(specifications['Підключення материнської плати'], '20+4 pin')
        self.assertEqual(specifications['Підключення процесора'], '2x4+4 pin')
        self.assertEqual(specifications['Підключення відеокарти'], '4x6+2 pin')
        self.assertEqual(specifications['Output Current +12V'], '58A')
        self.assertEqual(specifications['Захист від'], 'OPP, SCP, UVP, OVP')
        self.assertEqual(specifications['Розмір, мм'], '140 x 150 x 86 мм')
        self.assertEqual(specifications['Виробник'], 'Seasonic')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс'], 12)
        self.assertEqual(specifications['Штрихкод'], '4823093320123')
        self.assertEqual(specifications['Примітка'], 'Виробник може змінювати властивості.')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики', 'Інші'],
        )
        self.assertContains(response, 'data-open-specifications')
        self.assertContains(response, 'specifications-dialog')

    def test_power_supply_product_page_falls_back_to_shared_country_and_warranty(self):
        Product.objects.filter(pk=self.modular_gold_psu.pk).update(
            psu_country_of_origin='',
            psu_warranty_months=None,
        )

        response = self.client.get(
            reverse('product_detail', args=(self.modular_gold_psu.pk,)),
        )

        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс'], 12)


class CoolingCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Комплектуючі для ПК')
        self.liquid_cooler = Product.objects.create(
            name='Arctic Liquid Freezer III 360',
            category=self.category,
            component_type='cooling',
            price=Decimal('4800.00'),
            cooling_manufacturer='Arctic',
            cooling_cpu_compatibility='INTEL, AMD',
            cooling_socket='1700, AM4, AM5',
            cooling_fan_count='3',
            cooling_fan_diameter='120 мм',
            cooling_lighting='ARGB',
            cooling_max_tdp='350 Вт',
            cooling_max_fan_speed='2500 об/хв',
            cooling_radiator_material='алюміній',
            cooling_airflow='80.95 CFM',
            cooling_fan_speed_control='так',
            cooling_pump_power_connector='3-pin (помпа)',
            cooling_fan_power_connector='4-pin (вентилятор)',
            cooling_pump_voltage='12 В',
            cooling_tube_length='380 мм',
            cooling_radiator_dimensions='272 x 121 x 27 мм',
            cooling_fan_dimensions='120 x 120 x 25 мм',
            cooling_pump_dimensions='80 x 80 x 45 мм',
            cooling_noise_level='28 дБ',
            cooling_color='чорний',
            cooling_country_of_origin='Китай',
            cooling_warranty_months=120,
            cooling_barcode='4711081886754',
            cooling_note='Виробник може змінювати властивості.',
        )
        self.air_cooler = Product.objects.create(
            name='Noctua NH-U12S',
            category=self.category,
            component_type='cooling',
            price=Decimal('3200.00'),
            cooling_manufacturer='Noctua',
            cooling_cpu_compatibility='INTEL, AMD',
            cooling_socket='1151, 1200, 1700, AM4',
            cooling_fan_count='1',
            cooling_fan_diameter='120 мм',
            cooling_lighting='немає',
            cooling_max_tdp='250 Вт',
            cooling_noise_level='22 дБ',
            cooling_color='шампань',
        )
        Product.objects.create(
            name='PSU excluded from cooling filters',
            category=self.category,
            component_type='power_supply',
            price=Decimal('5000.00'),
            cooling_manufacturer='Arctic',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_cooling_catalog_shows_filter_groups_and_dynamic_noise_buckets(self):
        response = self.client.get(self.url, {'component_type': 'cooling'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['cooling_catalog'])
        self.assertEqual(
            list(response.context['products']),
            [self.air_cooler, self.liquid_cooler],
        )
        self.assertEqual(len(response.context['filter_groups']), 9)
        self.assertContains(response, 'Arctic (1)')
        self.assertContains(response, 'INTEL (2)')
        self.assertContains(response, 'AM5 (1)')
        self.assertContains(response, '3 (1)')
        self.assertContains(response, 'ARGB (1)')
        self.assertContains(response, '350 Вт (1)')
        self.assertContains(response, 'менше 25 дБ (1)')
        self.assertContains(response, '25 - 29 дБ (1)')

    def test_cooling_filters_combine_multi_values_and_noise_range(self):
        response = self.client.get(self.url, {
            'component_type': 'cooling',
            'cooling_manufacturer': 'Arctic',
            'cooling_cpu_compatibility': 'AMD',
            'cooling_socket': 'AM5',
            'cooling_fan_count': '3',
            'cooling_fan_diameter': '120 мм',
            'cooling_lighting': 'ARGB',
            'cooling_max_tdp': '350 Вт',
            'cooling_noise_level': '25 - 29 дБ',
            'cooling_color': 'чорний',
        })

        self.assertEqual(list(response.context['products']), [self.liquid_cooler])


    def test_cooling_catalog_price_filter_and_admin_fields(self):
        response = self.client.get(self.url, {
            'component_type': 'cooling',
            'price_max': '3500',
        })
        self.assertEqual(list(response.context['products']), [self.air_cooler])

        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
            if field_name.startswith('cooling_')
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('cooling_')
        }
        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(set(admin_fields), model_fields)

    def test_cooling_product_page_shows_grouped_specifications(self):
        response = self.client.get(
            reverse('product_detail', args=(self.liquid_cooler.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Для процесорів'], 'INTEL, AMD')
        self.assertEqual(specifications['Сокет'], '1700, AM4, AM5')
        self.assertEqual(specifications['Кількість вентиляторів'], '3')
        self.assertEqual(specifications['Максимальна частота обертів'], '2500 об/хв')
        self.assertEqual(specifications['Матеріал радіатора'], 'алюміній')
        self.assertEqual(specifications['Повітряний потік'], '80.95 CFM')
        self.assertEqual(specifications['Управління швидкістю обертання'], 'так')
        self.assertEqual(specifications['Роз’єм живлення помпи'], '3-pin (помпа)')
        self.assertEqual(specifications['Роз’єм живлення вентиляторів'], '4-pin (вентилятор)')
        self.assertEqual(specifications['Напруга живлення'], '12 В')
        self.assertEqual(specifications['Довжина патрубків'], '380 мм')
        self.assertEqual(specifications['Максимальний TDP'], '350 Вт')
        self.assertEqual(specifications['Рівень шуму'], '28 дБ')
        self.assertEqual(specifications['Розміри радіатора'], '272 x 121 x 27 мм')
        self.assertEqual(specifications['Розміри вентиляторів'], '120 x 120 x 25 мм')
        self.assertEqual(specifications['Розмір водоблоку'], '80 x 80 x 45 мм')
        self.assertEqual(specifications['Виробник'], 'Arctic')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс'], 120)
        self.assertEqual(specifications['Штрихкод'], '4711081886754')
        self.assertEqual(specifications['Примітка'], 'Виробник може змінювати властивості.')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            [
                'Основні характеристики',
                'Додаткові характеристики',
                'Фізичні характеристики',
                'Інші',
            ],
        )


class MonitorCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Монітори')
        self.monitor = Product.objects.create(
            name='AOC Gaming Monitor',
            category=self.category,
            price=Decimal('8999.00'),
            manufacturer='Vinga',
            display_diagonal='27"',
            matrix_type='IPS',
            resolution='2560 x 1440',
            refresh_rate='165 Гц',
            screen_surface='матове',
            interfaces='HDMI, DisplayPort, USB Type-C',
            built_in_speakers='є',
            webcam='немає',
            color='чорний',
            country_of_origin='Китай',
            warranty_months=12,
            features='Виробник може змінювати властивості, характеристики, зовнішній вигляд і комплектацію товарів без попередження',
            monitor_display_type='Широкоформатний, безрамковий',
            monitor_aspect_ratio='16:9',
            monitor_backlight='LED',
            monitor_response_time='менше 1 мс',
            monitor_brightness='250 кд/м2',
            monitor_static_contrast='1000:1',
            monitor_dynamic_contrast='10 000 000:1',
            monitor_viewing_angles='178/178',
            monitor_max_colors='16.7 млн',
            monitor_image_enhancement='Low Blue Light, Flicker Free',
            monitor_sync_technology='AMD FreeSync',
            monitor_stand_adjustment='регулювання по висоті, регулювання нахилу',
            monitor_tilt_angle='-5° - +15° (±3°)',
            monitor_vesa='100x100 мм',
            monitor_power_consumption='20.7 Вт',
            monitor_standby_power='0.4 Вт',
            monitor_dimensions_with_stand='542 x 380 x 200 мм',
            monitor_dimensions_without_stand='542 x 326 x 48 мм',
            monitor_weight_unboxed='2.85 кг',
            monitor_weight_boxed='3.5 кг',
        )
        self.other_category_product = Product.objects.create(
            name='AOC laptop, not monitor',
            category=Category.objects.create(name='Ноутбуки'),
            price=Decimal('9999.00'),
            manufacturer='AOC',
            monitor_aspect_ratio='16:9',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_monitor_catalog_shows_filter_groups_and_dynamic_values(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter_groups']), 15)
        self.assertEqual(list(response.context['products']), [self.monitor])
        self.assertContains(response, 'Vinga (1)')
        self.assertContains(response, 'менше 1мс (1)')
        self.assertContains(response, 'DisplayPort (1)')
        self.assertNotContains(response, 'AOC laptop, not monitor')

    def test_monitor_catalog_combines_filters_and_response_time_range(self):
        response = self.client.get(self.url, {
            'manufacturer': 'Vinga',
            'monitor_aspect_ratio': '16:9',
            'interfaces': 'DisplayPort',
            'monitor_response_time': 'менше 1мс',
            'monitor_vesa': '100x100 мм',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), [self.monitor])

    def test_monitor_filter_form_has_expected_fields(self):
        form = MonitorProductFilterForm(products=Product.objects.filter(category=self.category))

        self.assertEqual(
            [field_name for field_name, _ in form.filter_fields],
            [
                'manufacturer',
                'display_diagonal',
                'matrix_type',
                'resolution',
                'refresh_rate',
                'monitor_aspect_ratio',
                'monitor_backlight',
                'screen_surface',
                'monitor_response_time',
                'interfaces',
                'monitor_stand_adjustment',
                'monitor_vesa',
                'built_in_speakers',
                'webcam',
                'color',
            ],
        )

    def test_monitor_product_page_shows_reference_specification_groups(self):
        response = self.client.get(reverse('product_detail', args=(self.monitor.pk,)))

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Тип монітора'], 'Широкоформатний, безрамковий')
        self.assertEqual(specifications['Діагональ екрана'], '27"')
        self.assertEqual(specifications['Контрастність статична'], '1000:1')
        self.assertEqual(specifications['Технології синхронізації'], 'AMD FreeSync')
        self.assertEqual(
            specifications['Споживана потужність у робочому режимі'],
            '20.7 Вт',
        )
        self.assertEqual(specifications['Інтерфейси та підключення'], 'HDMI, DisplayPort, USB Type-C')
        self.assertEqual(specifications['Регулювання нахилу'], '-5° - +15° (±3°)')
        self.assertEqual(specifications['Розміри з підставкою'], '542 x 380 x 200 мм')
        self.assertEqual(specifications['Виробник'], 'Vinga')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс'], 12)
        self.assertEqual(specifications['Колір'], 'чорний')
        self.assertEqual(
            specifications['Примітка'],
            'Виробник може змінювати властивості, характеристики, зовнішній вигляд і комплектацію товарів без попередження',
        )
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            [
                'Основні характеристики',
                'Роз’єми й інтерфейси',
                'Електричні параметри',
                'Додатково',
                'Фізичні характеристики',
                'Інші',
            ],
        )

    def test_monitor_admin_fields_are_unique_and_present(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
        ]
        model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('monitor_')
        }
        monitor_group = dict(ProductAdmin.fieldsets)['Характеристики монітора']['fields']
        expected_monitor_fields = {
            'display_diagonal',
            'matrix_type',
            'resolution',
            'refresh_rate',
            'screen_surface',
            'interfaces',
            'built_in_speakers',
        }
        network_group = dict(ProductAdmin.fieldsets)['Характеристики мережевого обладнання']['fields']
        expected_general_fields = {
            'manufacturer',
            'country_of_origin',
            'warranty_months',
            'features',
            'network_barcode',
            'network_note',
        }

        self.assertNotIn('Спільні характеристики товару', dict(ProductAdmin.fieldsets))
        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertTrue(model_fields.issubset(set(admin_fields)))
        self.assertTrue(expected_monitor_fields.issubset(set(monitor_group)))
        self.assertTrue(expected_general_fields.issubset(set(admin_fields)))


class NetworkCatalogFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Мережеві фільтри та подовжувачі')
        self.extension = Product.objects.create(
            name='ColorWay extension cord',
            category=self.category,
            price=Decimal('1200.00'),
            manufacturer='ColorWay',
            network_product_type='мережеві подовжувачі',
            network_socket_count='5',
            network_outlet_type='євро-розетка із заземленням (Тип F)',
            network_input_plug_type='євровилка із заземленням (Тип F)',
            network_usb_ports='2 x USB (type A)',
            network_cable_length='1.8 м',
            network_features='з вимикачем на кожну розетку, захист від перенапруги',
            network_protection='від дітей, від короткого замикання',
            network_total_power='≤ 3500 Вт',
            color='чорний',
        )
        self.power_filter = Product.objects.create(
            name='Defender power filter',
            category=self.category,
            price=Decimal('700.00'),
            manufacturer='Defender',
            network_product_type='мережеві фільтри живлення',
            network_socket_count='3',
            network_outlet_type='універсальна розетка',
            network_input_plug_type='євровилка із заземленням (Тип F)',
            network_usb_ports='1 x USB (type A)',
            network_cable_length='3 м',
            network_features='із загальним вимикачем',
            network_protection='від перевантаження',
            network_total_power='≤ 2200 Вт',
            color='білий',
        )
        Product.objects.create(
            name='Unclassified network product',
            category=self.category,
            price=Decimal('500.00'),
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_network_catalog_shows_preset_and_dynamic_options_without_gray_items(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [group['name'] for group in response.context['filter_groups']],
            [
                'Тип',
                'Кількість розеток',
                'Тип вихідних розеток',
                'Тип вхідної вилки',
                'USB порти',
                'Довжина кабелю',
                'Особливості',
                'Захист',
                'Сумарна потужність підключеного навантаження',
                'Виробник',
                'Колір',
            ],
        )
        self.assertContains(response, 'мережеві подовжувачі (1)')
        self.assertContains(response, 'мережеві фільтри живлення (1)')
        self.assertContains(response, '5 (1)')
        self.assertContains(response, '3 (1)')
        self.assertContains(response, '2 x USB (type A) (1)')
        self.assertContains(response, '1.8 м (1)')
        self.assertContains(response, 'ColorWay (1)')
        self.assertContains(response, 'Defender (1)')
        self.assertContains(response, 'чорний (1)')
        self.assertNotContains(response, 'Acer')
        self.assertContains(response, 'мережевий розгалужувач')
        self.assertNotContains(response, '15 м')
        self.assertNotContains(response, '≤ 5000 Вт')
        self.assertNotContains(response, 'помаранчевий')

    def test_network_catalog_filters_by_type_manufacturer_specs_and_price(self):
        response = self.client.get(self.url, {
            'network_product_type': 'мережеві подовжувачі',
            'network_socket_count': '5',
            'network_usb_ports': '2 x USB (type A)',
            'network_features': 'з вимикачем на кожну розетку',
            'network_protection': 'від дітей',
            'manufacturer': 'ColorWay',
            'price_min': '1000',
            'price_max': '1500',
        })

        self.assertEqual(list(response.context['products']), [self.extension])

    def test_network_filter_form_shows_reference_options_without_products_or_gray_items(self):
        form = NetworkProductFilterForm(
            products=Product.objects.filter(
                category=self.category,
                name='No products match this filter',
            ),
        )

        manufacturer_values = [value for value, _ in form.fields['manufacturer'].choices]
        self.assertIn('ColorWay', manufacturer_values)
        self.assertIn('Defender', manufacturer_values)
        self.assertIn('XoKo', manufacturer_values)
        self.assertNotIn('Delux', manufacturer_values)

        cable_lengths = [
            value
            for value, _ in form.fields['network_cable_length'].choices
        ]
        self.assertIn('1.8 м', cable_lengths)
        self.assertNotIn('15 м', cable_lengths)

        protection_values = [
            value
            for value, _ in form.fields['network_protection'].choices
        ]
        self.assertIn('IP20', protection_values)
        self.assertNotIn('IP40', protection_values)

        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
        ]
        self.assertEqual(admin_fields.count('network_product_type'), 1)

    def test_network_product_detail_shows_reference_specification_groups(self):
        Product.objects.filter(pk=self.extension.pk).update(
            network_cable_specification='3*1.5 мм²',
            network_filter_material='вогнестійкий пластик',
            network_additional_features='кріплення на стіну',
            network_nominal_voltage='~250 В (макс)',
            network_breaker_trip_current='16 А',
            country_of_origin='Китай',
            warranty_months=36,
            network_barcode='4823108630551',
            network_note='Виробник може змінювати властивості.',
        )

        response = self.client.get(reverse('product_detail', args=(self.extension.pk,)))

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Тип'], 'мережеві подовжувачі')
        self.assertEqual(specifications['Кількість розеток'], '5')
        self.assertEqual(specifications['Тип вихідних розеток'], 'євро-розетка із заземленням (Тип F)')
        self.assertEqual(specifications['Довжина кабелю'], '1.8 м')
        self.assertEqual(specifications['Технічні характеристики кабелю'], '3*1.5 мм²')
        self.assertEqual(specifications['Матеріал фільтра'], 'вогнестійкий пластик')
        self.assertEqual(specifications['Додаткові характеристики'], 'кріплення на стіну')
        self.assertEqual(specifications['Номінальна напруга'], '~250 В (макс)')
        self.assertEqual(specifications['Струм спрацьовування термозапобіжника'], '16 А')
        self.assertEqual(specifications['Виробник'], 'ColorWay')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Гарантія, міс'], 36)
        self.assertEqual(specifications['Штрихкод'], '4823108630551')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики'],
        )
        self.assertContains(response, 'specifications-dialog')

    def test_network_admin_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
        ]
        network_admin_fields = {
            field_name for field_name in admin_fields
            if field_name.startswith('network_')
        }
        network_model_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('network_')
        }
        network_fields = dict(ProductAdmin.fieldsets)['Характеристики мережевого обладнання']['fields']

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(network_admin_fields, network_model_fields)
        self.assertTrue({
            'network_barcode',
            'network_note',
            'color',
            'manufacturer',
            'country_of_origin',
            'warranty_months',
            'features',
        }.issubset(set(network_fields)))

    def test_empty_network_catalog_still_shows_filter_options(self):
        Product.objects.filter(category=self.category).delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['filter_groups']), 11)
        self.assertContains(response, 'ColorWay')
        self.assertContains(response, '1.8 м')


class ThermalPasteCatalogTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Обслуговування ПК')
        self.thermal_paste = Product.objects.create(
            name='Arctic MX-4 4 г',
            category=self.category,
            price=Decimal('218.00'),
            thermal_manufacturer='Arctic',
            thermal_compatibility='для процесорів, для ноутбука, для відеокарти',
            thermal_conductivity='8.5 W/mK',
            thermal_weight='4 г',
            thermal_packaging='шприц',
            thermal_country_of_origin='Китай',
            thermal_barcode='4895213701655',
            thermal_note='Виробник може змінювати властивості.',
        )
        self.url = reverse('category_products', args=(self.category.pk,))

    def test_empty_thermal_paste_catalog_shows_preset_options_and_service_link(self):
        self.thermal_paste.delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [group['name'] for group in response.context['filter_groups']],
            ['Виробник', 'Сумісність', 'Теплопровідність', 'Вага', 'Тип упаковки'],
        )
        self.assertContains(response, 'Arctic')
        self.assertContains(response, 'для процесорів')
        self.assertContains(response, '8.5 W/mK')
        self.assertContains(response, '4 г')
        self.assertContains(response, 'шприц')
        self.assertContains(response, 'Обслуговування ПК')
        self.assertContains(response, 'Термопаста, очищення та догляд за комп’ютером')

    def test_thermal_pastes_category_alias_also_shows_filters(self):
        category = Category.objects.create(name='Термопасти')

        response = self.client.get(reverse('category_products', args=(category.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [group['name'] for group in response.context['filter_groups']],
            ['Виробник', 'Сумісність', 'Теплопровідність', 'Вага', 'Тип упаковки'],
        )

    def test_thermal_paste_filters_combine_price_and_specifications(self):
        response = self.client.get(self.url, {
            'thermal_manufacturer': 'Arctic',
            'thermal_compatibility': 'для ноутбука',
            'thermal_conductivity': '8.5 W/mK',
            'thermal_weight': '4 г',
            'thermal_packaging': 'шприц',
            'price_min': '200',
            'price_max': '250',
        })

        self.assertEqual(list(response.context['products']), [self.thermal_paste])
        self.assertContains(response, 'Arctic (1)')
        self.assertContains(response, 'для ноутбука (1)')
        self.assertContains(response, 'шприц (1)')

    def test_thermal_paste_product_page_shows_reference_specification_groups(self):
        response = self.client.get(
            reverse('product_detail', args=(self.thermal_paste.pk,)),
        )

        self.assertEqual(response.status_code, 200)
        specifications = dict(response.context['specifications'])
        self.assertEqual(specifications['Сумісність'], 'для процесорів, для ноутбука, для відеокарти')
        self.assertEqual(specifications['Теплопровідність'], '8.5 W/mK')
        self.assertEqual(specifications['Вага'], '4 г')
        self.assertEqual(specifications['Тип упаковки'], 'шприц')
        self.assertEqual(specifications['Виробник'], 'Arctic')
        self.assertEqual(specifications['Країна виробництва'], 'Китай')
        self.assertEqual(specifications['Штрихкод'], '4895213701655')
        self.assertEqual(
            [group['name'] for group in response.context['specification_groups']],
            ['Основні характеристики', 'Інші'],
        )

    def test_thermal_paste_admin_fields_are_grouped_without_duplicates(self):
        admin_fields = [
            field_name
            for _, options in ProductAdmin.fieldsets
            for field_name in options['fields']
        ]
        paste_fields = {
            field.name
            for field in Product._meta.fields
            if field.name.startswith('thermal_')
        }
        paste_admin_fields = {
            field_name for field_name in admin_fields
            if field_name.startswith('thermal_')
        }
        paste_group = dict(ProductAdmin.fieldsets)['Характеристики термопасти']['fields']

        self.assertEqual(len(admin_fields), len(set(admin_fields)))
        self.assertEqual(paste_admin_fields, paste_fields)
        self.assertEqual(set(paste_group), paste_fields)