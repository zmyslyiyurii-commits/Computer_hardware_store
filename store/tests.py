from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Order, OrderItem, Product, ProductImage


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