import unittest
from stricterBM import good_suffix_pre

class TestCases(unittest.TestCase):
    def test_case1(self):
        p = "acababacaba"
        index_arr = good_suffix_pre(s, p)
        self.assertEqual(index_arr, [6, 28], "Should be [6, 28]")