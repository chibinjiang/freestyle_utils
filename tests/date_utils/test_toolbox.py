import unittest
from freestyle_utils.date_utils.toolbox import get_utcnow


class UtcNowTest(unittest.TestCase):

    def test_get_utcnow(self):
        print("test_get_utcnow(): ", get_utcnow())

    def test_get_iso_now(self):
        print("test_get_iso_now(): ", get_utcnow(format='iso'))


if __name__ == '__main__':
    unittest.main()

