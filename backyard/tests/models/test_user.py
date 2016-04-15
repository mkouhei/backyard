# -*- coding: utf-8 -*-
import unittest
import transaction

from pyramid import testing

from ..models.base import DBSession


class TestUserSuccessCondition(unittest.TestCase):
    """Test case user model."""

    def setUp(self):
        """prepare."""
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models.base import Base
        from ..models.user import User
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = User(name='admin',
                         email='admin@example.org')
            DBSession.add(model)

    def tearDown(self):
        """clean up."""
        DBSession.remove()
        testing.tearDown()

    @unittest.skip
    def test_passing_view(self):
        """view test."""
        from backyard.views import user_view
        request = testing.DummyRequest()
        info = user_view(request)
        self.assertEqual(info['admin'].name, 'admin')
        self.assertEqual(info['email'], 'admin@example.org')


class TestUserFailureCondition(unittest.TestCase):
    """Failure Test case user model."""
    def setUp(self):
        """prepare."""
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models.base import Base
        from ..models.user import User
        DBSession.configure(bind=engine)

    def tearDown(self):
        """clean up."""
        DBSession.remove()
        testing.tearDown()

    @unittest.skip
    def test_failing_view(self):
        """view test."""
        from backyard.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info.status_int, 500)
