from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class CategoryProductsPageTests(TestCase):
    def setUp(self):
        self.laptops = Category.objects.create(name='Ноутбуки', icon='▱')
        self.accessories = Category.objects.create(name='Аксесуари', icon='⌘')
        self.laptop = Product.objects.create(
            name='Ноутбук для тесту',
            category=self.laptops,
            price='25000.00',
        )
        Product.objects.create(
            name='Миша для тесту',
            category=self.accessories,
            price='1000.00',
        )

    def test_category_page_shows_only_products_in_selected_category(self):
        response = self.client.get(
            reverse('category_products', args=[self.laptops.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Ноутбуки</h1>', html=True)
        self.assertContains(response, self.laptop.name)
        self.assertNotContains(response, 'Миша для тесту')
        self.assertContains(response, 'Виробник')
        self.assertContains(response, 'Варіанти фільтра буде додано')
        self.assertNotContains(response, 'breadcrumbs')
        self.assertContains(response, 'name="q"')

    def test_homepage_category_links_to_its_products(self):
        response = self.client.get(reverse('home'))

        self.assertContains(
            response,
            reverse('category_products', args=[self.laptops.pk]),
        )

    def test_missing_category_returns_404(self):
        response = self.client.get(
            reverse('category_products', args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_laptop_filters_are_not_shown_for_other_categories(self):
        response = self.client.get(
            reverse('category_products', args=[self.accessories.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Фільтри')

    def test_laptop_filters_are_shown_for_singular_category_name(self):
        singular_laptop_category = Category.objects.create(name='Ноутбук')

        response = self.client.get(
            reverse('category_products', args=[singular_laptop_category.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фільтри')
        self.assertContains(response, 'Виробник')