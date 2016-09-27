"""backyard.inventory.tests.querysets.test_ordered_history"""
from datetime import datetime
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from ...models.maker import Maker
from ...models.product import Product
from ...models.shop import Shop
from ...models.price_history import PriceHistory
from ...models.order_history import OrderHistory
from ...queryset.order_history import OrderQuerySet


class OrderQuerySetTest(TransactionTestCase):
    """OrderQuerySet tests."""
    fixtures = ['backyard/inventory/tests/data/users.json']

    def setUp(self):
        """initialize."""
        self.user = User.objects.get(pk=1)
        self.group = self.user.groups.get()
        self.now = datetime.now()
        shop = Shop(name='some shop', url='https://shop.example.com')
        shop.save()
        maker = Maker(name='some maker')
        maker.save()
        self.product = Product(name='some product', maker=maker)
        self.product.save()
        price = PriceHistory(product=self.product,
                             shop=shop,
                             registered_date=self.now,
                             price=1234)
        price.save()
        self.order = OrderHistory(product=self.product,
                                  price=price,
                                  ordered_quantity=10,
                                  ordered_at=self.now,
                                  owner=self.user,
                                  group=self.user.groups.get())
        self.order.save()

    def test_product_name(self):
        """test ordered product."""
        self.assertEqual(
            OrderQuerySet(self.product.id, self.group).product_name,
            'some product')

    def test_order(self):
        """test ordered product."""
        query = OrderQuerySet(self.product.id, self.group).order[0]
        self.assertEqual(query.get('price__price'), 1234)
        self.assertEqual(query.get('ordered_quantity'), 10)
