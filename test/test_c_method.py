import logging

from internal.c import MyClass
from tabeltests.utils import BaseTestClass, SubTest


class MyTestAccept(BaseTestClass):

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="This is accepted test for MyClass.plus method",
                object=MyClass(5),
                args={'b': 1},
                want=6,
            ),
            SubTest(
                name="Test 2",
                description="This is accepted test for MyClass.plus method",
                object=MyClass(5),
                args={'b': 2},
                want=7,
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.plus(**kwargs))


class MyTestException(BaseTestClass):

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="This is accepted test for MyClass.plus method",
                object=MyClass(5),
                args={'b': 1},
                exception=Exception,
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.raise_(**kwargs))
