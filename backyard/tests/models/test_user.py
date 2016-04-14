# -*- coding: utf-8 -*-
import unittest
import transaction

from pyramid import testing

from backyard.models.base import DBSession


class TestUserSuccessCondition(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from backyard.models.base import Base
        from backyard.models.user import User
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    @unittest.skip
    def test_passing_view(self):
        from backyard.views import user_view
        request = testing.DummyRequest()
        info = user_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'hoge')


class TestUserFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from backyard.models.base import Base
        from backyard.models.user import User
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    @unittest.skip
    def test_failing_view(self):
        from backyard.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info.status_int, 500)
