import logging

from internal.c import MyClass
from tabeltests.utils import BaseTestClass, SubTest


class MyTestException(BaseTestClass):

    def __check(self, obj, want):
        self.assertEqual(obj.a, want)

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="This test checks middlewares execute after exception",
                object=MyClass(5),
                args={'c': 1},
                object_processors=[
                    lambda obj: self.__check(obj, 1)
                ],
                ignore_want=True,
                exception=TypeError,
                middlewares_after=[
                    lambda: self.assert_true(lambda: True),
                ],
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.raise_(**kwargs))
