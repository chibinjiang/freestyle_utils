import unittest
from freestyle_utils.decorators.toolbox import retry, timeit


class DecoratorsTest(unittest.TestCase):

    def test_retry(self):
        print("test_get_utcnow(): ", retry)

    def test_timeit(self):
        print("test_get_iso_now(): ", timeit)


if __name__ == '__main__':
    unittest.main()

