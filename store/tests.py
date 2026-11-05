from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.admin import ProductAdminForm
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

        self.assertTrue(Category.objects.filter(name='Обслуговування ПК').exists())
        self.assertFalse(Category.objects.filter(name='Накопичувачі').exists())
        self.assertContains(response, 'Обслуговування ПК')
        self.assertContains(response, 'Термопаста, очищення та догляд за комп’ютером')
        self.assertNotContains(response, 'SSD, жорсткі диски та флешнакопичувачі')


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
        self.assertEqual(len(response.context['component_cards']), 8)
        for title in (
            'Процесори',
            'Материнські плати',
            'Відеокарти',
            "Оперативна пам’ять",
            'Накопичувачі SSD / HDD',
            'Корпуси',
            'Блоки живлення',
            'Системи охолодження',
        ):
            self.assertContains(response, title)
        component_titles = {component['title'] for component in response.context['component_cards']}
        self.assertNotIn('Монітори', component_titles)
        self.assertNotIn('Маніпулятори', component_titles)
        self.assertNotIn('Обслуговування ПК', component_titles)

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