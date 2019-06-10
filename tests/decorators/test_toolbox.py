import time
import unittest
from freestyle_utils.decorators.toolbox import retry, timeit


class DecoratorsTest(unittest.TestCase):

    def test_retry(self):
        def inner_func(s):
            print("Params: ", s)
            raise Exception("Test Retry by raise Exception")
        print("test_retry()")
        retry((Exception, ), tries=3, delay=2, backoff=2)(inner_func)("Zhibin Jiang")

    def test_timeit(self):
        def inner_func(s):
            print("Sleep 1 second")
            print("Params: ", s)
            time.sleep(1)
            print("Wakeup !")
        print("test_timeit(): ")
        timeit(inner_func)("Jiang Zhibin")


if __name__ == '__main__':
    """
    python -m tests.decorators.test_toolbox
    """
    unittest.main()

