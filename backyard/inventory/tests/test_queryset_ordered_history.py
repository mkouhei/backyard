"""backyard.inventory.tests.test_queryset"""
from datetime import datetime
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from backyard.inventory.models import (Maker,
                                       Product,
                                       Shop,
                                       PriceHistory,
                                       OrderHistory)
from backyard.inventory.queryset.order_history import OrderQuerySet


class OrderQuerySetTest(TransactionTestCase):
    """OrderQuerySet tests."""
    fixtures = ['backyard/inventory/tests/data/users.json']

    def setUp(self):
        """initialize."""
        self.user = User.objects.get(pk=1)
        shop = Shop(name='some shop', url='https://shop.example.com')
        shop.save()
        maker = Maker(name='some maker')
        maker.save()
        product = Product(name='some product', maker=maker)
        product.save()
        price = PriceHistory(product=product,
                             shop=shop,
                             registered_date=datetime.now(),
                             price=1234)
        price.save()
        self.order = OrderHistory(ordered_item=price,
                                  quantity=10,
                                  owner=self.user,
                                  group=self.user.groups.get())
        self.order.save()

    def test_ordered_product(self):
        """test ordered product."""
        self.assertEqual(OrderQuerySet(self.order).ordered_product().__str__(),
                         'some product')

    def test_product_price(self):
        """test ordered product."""
        self.assertEqual(OrderQuerySet(self.order).product_price(), 1234)

    def test_amount(self):
        """test amount."""
        self.assertEqual(OrderQuerySet(self.order).amount(), 12340)
