import logging

from tests.c import plus
from tabeltests.utils import BaseTestClass, SubTest


class MyTestAcceptFunc(BaseTestClass):

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="This is accepted test for function plus",
                args={'b': 1, 'a': 5},
                want=6,
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: plus(**kwargs))
