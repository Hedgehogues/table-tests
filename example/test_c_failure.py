import logging

from example.c import MyClass
from utils import BaseTestClass, SubTest


class MyTestAccept(BaseTestClass):

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="This is failure test",
                object=MyClass(5),
                args={'b': 1},
                want=5,
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.plus(**kwargs))
