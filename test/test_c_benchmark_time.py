import logging

from internal.c import MyClass
from tabeltests.utils import BaseTestClass, SubTest


class MyTestAccept(BaseTestClass):

    def __check(self, obj, want):
        self.assertEqual(obj.a, want)

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                object=MyClass(5),
                args={'b': 1},
                object_processors=[
                    lambda obj: self.__check(obj, 5)
                ],
                ignore_want=True,
                time_benchmark=True,
                num_time_benchmark=50,
                var_time_benchmark=7,
                mean_time_benchmark=7,
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.plus(**kwargs))