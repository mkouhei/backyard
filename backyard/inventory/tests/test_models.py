"""backyard.inventory.tests.test_models"""
from django.test import TransactionTestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from backyard.inventory.models import (Maker,
                                       Product,
                                       Shop,
                                       ExternalAccount)


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
        shop = Shop(name='some shop', url='https://shop.example.com')
        shop.save()
        self.query = ExternalAccount(name=self.user.username,
                                     email=self.user.email,
                                     owner=self.user,
                                     group=self.user.groups.get(),
                                     encrypted_password=self.user.password,
                                     shop=shop)
        self.query.save()

    def test_create(self):
        """create."""
        self.assertEqual(self.query.__str__(), self.user.username)
        self.assertEqual(self.query.email, self.user.email)
