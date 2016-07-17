"""backyard.inventory.tests.test_models"""
from django.test import TransactionTestCase
from django.db import IntegrityError
from backyard.inventory.models import (Maker,
                                       Product)


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
