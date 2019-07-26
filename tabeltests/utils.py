import json
import logging
import os
import time

import deepdiff
import unittest
import numpy as np


class BaseTestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.tests_parse = []

        # create formatter for benchmark
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch = logging.StreamHandler()
        self.ch.setFormatter(formatter)

    @staticmethod
    def __middleware(mws):
        for mw in mws:
            mw()

    def __time_benchmark(self, func, obj, test, logger):
        s = []
        for i in range(test.num_time_benchmark):
            t = time.process_time()
            func(obj, test.args)
            s.append(time.process_time() - t)
        logger.addHandler(self.ch)
        m = test.mean_time_benchmark
        v = test.var_time_benchmark
        f = f"mean time: %.{m}f. time variance: %.{v}f"
        logger.info(f % (float(np.mean(s)), float(np.sqrt(np.var(s)))))

    @staticmethod
    def __memory_benchmark(logger):
        logger.warning("not implemented memory benchmark")

    def __valid(self, test, func):
        res = func(test.object, test.args)
        logger = logging.getLogger('bench for %s' % test.name)
        logger.setLevel(logging.INFO)
        if test.time_benchmark:
            test.middlewares_after.append(lambda: self.__time_benchmark(func, test.object, test, logger))
        if test.memory_benchmark:
            test.middlewares_after.append(lambda: self.__memory_benchmark(logger))

        for p in test.answer_processors:
            res = p(res)
        for p in test.object_processors:
            p(test.object)
        self.__middleware(test.middlewares_after)
        if not test.ignore_want:
            diff = deepdiff.DeepDiff(test.want, res)
            self.assertEqual(0, len(diff), msg="want=%s, got=%s" % (test.want, res))

    def __exception(self, test, func):
        try:
            func(test.object, test.args)
            self.__middleware(test.middlewares_after)
        except Exception as e:
            self.__middleware(test.middlewares_after)
            self.assertTrue(type(e) == test.exception)
            return
        self.assertTrue(False)

    def assert_false(self, callback):
        """
        assert_false needs for check false callback

        for example, if you want to make integration tests, you need check result of middleware and clear environment:

        SubTest(
            name="test",
            middleware_after=[
                generate_data(),
            ],
            object=X,
            ignore_want=True,
            middlewares_after=[
                self.assert_false(generate_data),  # Here, we use this function
                clear_data(),
            ],
        ),

        :param callback:
        :return:
        """
        self.assertFalse(callback())

    def assert_true(self, callback):
        """
        assert_false needs for check true callback

        for example, if you want to make integration tests, you need check result of middleware:

        SubTest(
            name="test",
            middleware_after=[
                generate_data(),
            ],
            object=X,
            ignore_want=True,
            middlewares_after=[
                self.assert_true(generate_data),  # Here, we use this function
                clear_data(),
            ],
        ),

        :param callback:
        :return:
        """
        x = callback()
        self.assertTrue(x)

    def check_exist_file(self, filename):
        """
        :param filename: path to file (str)
        :return:
        """
        self.assertTrue(os.path.exists(filename))

    @staticmethod
    def remove_filename(filename):
        """
        :param filename: path to file (str)
        :return: nothing
        """
        if os.path.exists(filename):
            os.remove(filename)

    @staticmethod
    def create_filename(filename):
        """
        :param filename: path to file (str)
        :return: nothing
        """
        if not os.path.exists(filename):
            open(filename, 'w').close()

    def apply_test(self, test, func):
        if test.fail:
            self.fail()
        msg = test.create_msg()
        with self.subTest(msg=msg):
            self.__middleware(test.middlewares_before)
            if test.exception is None:
                self.__valid(test, func)
                return
            self.__exception(test, func)


class SubTest:

    """
    Table data for object. If you want to test single function, you can use closure (lambda wrapper)

    :param name (str): name of test
    :param args (dict): arguments tested function
    :param description (str): description of test
    :param object (object): description of test
    :param want (object): wanted answer from function
    :param ignore_want (bool): ignore returned value of function if exception is not state.
        If exception generates into function, want ignore don't need. This param can use for
        test of constructor for instance.
    :param exception (Exception): exception expected from function or None (if exception is not raises).
        If exception is state, then field lwant is ignore
    :param answers_processor (list): this function needs for process answers.
        For instance, suppose your function returns list of elements without range. Then you can sort your answer
        and check them after that
    :param object_processor (list): this function needs for process of object.
        For instance, suppose your function save the state or has mock object, which save data. Then you needs
    :param middlewares_before (list): list of middlewares functions which execute before start functionall unittests methods. Response from middleware not processed.
        For instance, you can add function which open file or create additional objects
    :param middlewares_before (list): list of middlewares functions which execute after finished function.
        For instance, you can add function which close file or remove additional objects
    :param fail (bool): is true, then test will be fail
    :param time_benchmark (bool): does need to use time benchmark
    :param num_time_benchmark (int): number of program launches for time benchmark estimation (default=5)
    :param mean_eps_time_benchmark (int): a number of symbols after comma for mean time (default=15)
    :param var_eps_time_benchmark (int): a number of symbols after comma for time variance (default=15)
    :param memory_benchmark (bool): does need to use memory benchmark
    :param num_memory_benchmark (int): number of program launches for time benchmark estimation (default=5)
    :param mean_eps_memory_benchmark (int): a number of symbols after comma for mean time (default=15)
    :param var_eps_memory_benchmark (int): a number of symbols after comma for time variance (default=15)

    self.configuration = self.fill('configuration', None, kwargs)
    """

    def __init__(self, **kwargs):
        # Name of data
        self.name = self.fill('name', 'Default name test', kwargs)
        # Description of data
        self.description = self.fill('description', None, kwargs)
        # Arguments tested function
        self.args = self.fill('args', {}, kwargs)
        # Test function (need lambda wrapper) or data method of object
        self.object = self.fill('object', None, kwargs)
        # Wanted answer
        self.want = self.fill('want', None, kwargs)
        # Ignore want
        self.ignore_want = self.fill('ignore_want', False, kwargs)
        # Wanted exception or None
        self.exception = self.fill('exception', None, kwargs)
        # Answer's process of target function with a callback function.
        # After that answer pass for check
        self.answer_processors = self.fill('answer_processors', [], kwargs)
        self.object_processors = self.fill('object_processors', [], kwargs)
        self.middlewares_before = self.fill('middlewares_before', [], kwargs)
        self.middlewares_after = self.fill('middlewares_after', [], kwargs)
        self.configuration = self.fill('configuration', None, kwargs)
        self.fail = self.fill('fail', False, kwargs)
        self.time_benchmark = self.fill('time_benchmark', False, kwargs)
        self.memory_benchmark = self.fill('memory_benchmark', False, kwargs)
        self.mean_time_benchmark = self.fill('mean_time_benchmark', 15, kwargs)
        self.mean_memory_benchmark = self.fill('mean_memory_benchmark', 15, kwargs)
        self.var_time_benchmark = self.fill('var_time_benchmark', 15, kwargs)
        self.var_memory_benchmark = self.fill('var_memory_benchmark', 15, kwargs)
        self.num_time_benchmark = self.fill('num_time_benchmark', 5, kwargs)
        self.num_memory_benchmark = self.fill('num_memory_benchmark', 5, kwargs)

    @staticmethod
    def fill(k, r, kwargs):
        return kwargs[k] if k in kwargs else r

    def create_msg(self):
        descr = self.description
        msg = self.name + '. '
        if descr is not None:
            msg += 'Description: %s. ' % descr
        if self.configuration is not None:
            msg += 'Configuration: %s. ' % json.dumps(self.configuration)
        return msg
