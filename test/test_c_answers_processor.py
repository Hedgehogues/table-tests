import logging

from internal.c import MyClass
from tabeltests.utils import BaseTestClass, SubTest


class MyTestAccept(BaseTestClass):

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="This test adds two numbers and after that add 1 else",
                object=MyClass(5),
                args={'b': 1},
                want=7,
                answer_processors=[lambda x: x + 1],
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.plus(**kwargs))
