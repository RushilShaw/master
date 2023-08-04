import unittest

import os
import subprocess


class MyTestCase(unittest.TestCase):
    def test_gps_starter(self):
        result = os.system(r'python3 master.py')
        self.assertEqual(result, "PY_SUCCESS")  # add assertion here


if __name__ == '__main__':
    unittest.main()
