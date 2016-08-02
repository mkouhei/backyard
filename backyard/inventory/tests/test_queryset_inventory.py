"""backyard.inventory.tests.test_queryset_inventory"""
from datetime import datetime
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from backyard.inventory.models import (Maker,
                                       Product,
                                       Shop,
                                       PriceHistory,
                                       OrderHistory,
                                       ReceiveHistory,
                                       UnpackHistory,
                                       Inventory)
from backyard.inventory.queryset.order_history import OrderQuerySet
from backyard.inventory.queryset.inventory import QuantityQuerySet


class QuantityQuerySetTest(TransactionTestCase):
    """QuantitiyQuerySet tests."""
    fixtures = ['backyard/inventory/tests/data/users.json']

    def setUp(self):
        """initialize."""
        self.user = User.objects.get(pk=1)
        shop = Shop(name='some shop', url='https://shop.example.com')
        shop.save()
        maker = Maker(name='some maker')
        maker.save()
        self.product = Product(name='some product', maker=maker)
        self.product.save()
        price = PriceHistory(product=self.product,
                             shop=shop,
                             registered_date=datetime.now(),
                             price=1234)
        price.save()
        self.order = OrderHistory(ordered_item=price,
                                  quantity=10,
                                  owner=self.user,
                                  group=self.user.groups.get())
        self.order.save()
        self.received = ReceiveHistory.objects.get(
            received_item=self.order)
        self.received.quantity = 6
        self.received.save()
        self.unpacked = UnpackHistory.objects.get(
            unpacked_item=OrderQuerySet(self.order).ordered_product)
        self.unpacked.quantity = 4
        self.unpacked.save()
        self.inventory = Inventory.objects.get(product=self.product)

    def test_ordered_item(self):
        """test ordered_item."""
        self.assertTrue(
            'some product 1234 * 10' in
            QuantityQuerySet(self.inventory).ordered_item.__str__())

    def test_ordered_quantity(self):
        """test ordered_quantity."""
        self.assertEqual(QuantityQuerySet(self.inventory).ordered_quantity,
                         10)

    def test_received_quantity(self):
        """test received_quantity."""
        self.assertEqual(QuantityQuerySet(self.inventory).received_quantity,
                         6)

    def test_unpacked_quantity(self):
        """test unpacked_quantity."""
        self.assertEqual(QuantityQuerySet(self.inventory).unpacked_quantity,
                         4)

    def test_remain_quantity(self):
        """test remain_quantity."""
        self.assertEqual(QuantityQuerySet(self.inventory).remain_quantity,
                         2)
