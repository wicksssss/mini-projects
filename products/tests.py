from django.test import TestCase
from .models import Category, Brand, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Face Care',
            slug='face-care',
            is_active=True
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Face Care')

    def test_category_is_active(self):
        self.assertTrue(self.category.is_active)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Face Care',
            slug='face-care',
            is_active=True
        )
        self.brand = Brand.objects.create(
            name="L'Oreal",
            slug='loreal'
        )
        self.product = Product.objects.create(
            name='Face Cream',
            slug='face-cream',
            price=299.00,
            discount_price=249.00,
            stock=10,
            category=self.category,
            brand=self.brand,
            is_active=True
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Face Cream')

    def test_get_discount_percent(self):
        percent = self.product.get_discount_percent()
        self.assertEqual(percent, 17)

    def test_is_available(self):
        self.assertTrue(self.product.is_available())

    def test_is_not_available_when_no_stock(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_available())

    def test_product_manager_active(self):
        active = Product.objects.active()
        self.assertIn(self.product, active)
