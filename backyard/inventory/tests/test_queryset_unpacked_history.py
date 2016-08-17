"""backyard.inventory.tests.test_queryset_unpacked_history"""
from datetime import datetime
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from ..models.maker import Maker
from ..models.product import Product
from ..models.shop import Shop
from ..models.price_history import PriceHistory
from ..models.order_history import OrderHistory
from ..models.receive_history import ReceiveHistory
from ..models.unpack_history import UnpackHistory
from ..queryset.order_history import OrderQuerySet
from ..queryset.unpacked_history import UnpackQuerySet


class UnpackQuerySetTest(TransactionTestCase):
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
        self.received = ReceiveHistory(
            received_item=self.order,
            quantity=0,
            owner=self.user,
            group=self.user.groups.get()
        )
        self.received.save()
        self.unpacked = UnpackHistory(
            unpacked_item=OrderQuerySet(self.order).ordered_product,
            quantity=0,
            owner=self.user,
            group=self.user.groups.get()
        )
        self.unpacked.save()

    def test_ordered_quantity(self):
        """test ordered quantity."""
        self.assertEqual(UnpackQuerySet(self.unpacked).ordered_quantity, 10)
