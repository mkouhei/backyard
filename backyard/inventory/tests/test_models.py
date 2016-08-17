"""backyard.inventory.tests.test_models"""
from datetime import datetime
from django.test import TransactionTestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from backyard.inventory.models import (Maker,
                                       Product,
                                       Shop,
                                       ExternalAccount,
                                       PriceHistory,
                                       OrderHistory,
                                       ReceiveHistory,
                                       UnpackHistory)
from backyard.inventory.queryset.order_history import OrderQuerySet


class MakerTransactionTest(TransactionTestCase):
    """transaction test of Maker."""

    def setUp(self):
        self.maker_name = 'someone maker'
        self.query = Maker(name=self.maker_name)
        self.query.save()

    def test_create(self):
        """create."""
        self.assertEqual(self.query.__str__(), self.maker_name)

    def test_create_fail(self):
        """create fail."""
        query = Maker(name=self.maker_name)
        with self.assertRaises(IntegrityError):
            query.save()


class ProductTransactionTest(TransactionTestCase):
    """transaction test of Product."""

    def setUp(self):
        """initialize."""
        self.maker = Maker(name='some maker')
        self.maker.save()
        self.product_name = 'some product'
        self.query = Product(name=self.product_name, maker=self.maker)
        self.query.save()

    def test_create(self):
        """create."""
        self.assertEqual(self.query.__str__(), self.product_name)
        self.assertEqual(self.query.maker, self.maker)

    def test_create_fail(self):
        """create fail."""
        query = Product(name=self.product_name, maker=self.maker)
        with self.assertRaises(IntegrityError):
            query.save()


class ShopTransactionTest(TransactionTestCase):
    """transaction test of Shop."""

    def setUp(self):
        """initialize."""
        self.name = 'some shop'
        self.url = 'https://shop.example.com'
        self.query = Shop(name=self.name, url=self.url)
        self.query.save()

    def test_create(self):
        """create."""
        self.assertEqual(self.query.__str__(), self.name)
        self.assertEqual(self.query.url, self.url)

    def test_create_fail(self):
        """create fail."""
        query = Shop(name=self.name, url=self.url)
        with self.assertRaises(IntegrityError):
            query.save()


class ExternalAccountTest(TransactionTestCase):
    """transaction test of ExternalAccount."""
    fixtures = ['backyard/inventory/tests/data/users.json']

    def setUp(self):
        """initialize."""
        self.user = User.objects.get(pk=1)
        self.shop = Shop(name='some shop', url='https://shop.example.com')
        self.shop.save()
        self.query = ExternalAccount(name=self.user.username,
                                     email=self.user.email,
                                     owner=self.user,
                                     group=self.user.groups.get(),
                                     encrypted_password=self.user.password,
                                     shop=self.shop)
        self.query.save()

    def test_create(self):
        """create."""
        self.assertEqual(self.query.__str__(), self.user.username)
        self.assertEqual(self.query.email, self.user.email)

    def test_create_fail(self):
        """create fail."""
        self.query = ExternalAccount(name=self.user.username,
                                     email=self.user.email,
                                     owner=self.user,
                                     group=self.user.groups.get(),
                                     encrypted_password=self.user.password,
                                     shop=self.shop)
        with self.assertRaises(IntegrityError):
            self.query.save()


class PriceHistoryTest(TransactionTestCase):
    """transaction test of PriceHistory."""

    def setUp(self):
        """initialize."""
        self.shop = Shop(name='some shop', url='https://shop.example.com')
        self.shop.save()
        maker = Maker(name='some maker')
        maker.save()
        self.product = Product(name='some product', maker=maker)
        self.product.save()
        self.now = datetime.now()
        self.query = PriceHistory(product=self.product,
                                  shop=self.shop,
                                  registered_date=self.now,
                                  price=1234)
        self.query.save()

    def test_create(self):
        """create."""
        self.assertEqual(self.query.__str__(), 'some product 1234')

    def test_create_fail(self):
        """create fail."""
        self.query = PriceHistory(product=self.product,
                                  shop=self.shop,
                                  registered_date=self.now,
                                  price=1234)
        with self.assertRaises(IntegrityError):
            self.query.save()


class OrderHistoryTest(TransactionTestCase):
    """transaction test of OrderHistory."""
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
        self.received = None
        self.unpacked = None

    def test_create(self):
        """create."""
        self.assertTrue('some product 1234 * 10' in self.order.__str__())
        self.received = ReceiveHistory(
            received_item=self.order,
            quantity=6,
            owner=self.user,
            group=self.user.groups.get()
        )
        self.received.save()
        self.assertEqual(self.received.quantity, 6)
        self.assertTrue('some product 1234 * 10' in self.received.__str__())
        self.unpacked = UnpackHistory(
            unpacked_item=OrderQuerySet(self.order).ordered_product,
            quantity=4,
            owner=self.user,
            group=self.user.groups.get()
        )
        self.unpacked.save()
        self.assertEqual(self.unpacked.quantity, 4)
        self.assertEqual('some product', self.unpacked.__str__())

    def test_invalid_receive_quantity(self):
        """fail to create."""
        self.assertTrue('some product 1234 * 10' in self.order.__str__())
        self.received = ReceiveHistory(
            received_item=self.order,
            quantity=11,
            owner=self.user,
            group=self.user.groups.get()
        )
        self.received.quantity = 11
        with self.assertRaises(ValidationError):
            self.received.save()

    def test_invalid_unpacked_quantity(self):
        """create."""
        self.assertTrue('some product 1234 * 10' in self.order.__str__())
        self.received = ReceiveHistory(
            received_item=self.order,
            quantity=6,
            owner=self.user,
            group=self.user.groups.get()
        )
        self.received.save()
        self.assertEqual(self.received.quantity, 6)
        self.assertTrue('some product 1234 * 10' in self.received.__str__())
        self.unpacked = UnpackHistory(
            unpacked_item=OrderQuerySet(self.order).ordered_product,
            quantity=7,
            owner=self.user,
            group=self.user.groups.get()
        )
        with self.assertRaises(ValidationError):
            self.unpacked.save()
