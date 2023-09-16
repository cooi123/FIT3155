import unittest
from stricterBM import boyer_moore


class TestCases(unittest.TestCase):
    def test_case1(self):
        s = "acxcbbacababacabaaaabacabaafacababacaba"
        p = "acababacaba"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [6, 28], "Should be [6, 28]")

    def test_case2(self):
        s = "ababcababcabcabc"
        p = "abcabc"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [7, 10], (s, p))

    def test_case3(self):
        s = "mississippi"
        p = "issip"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [4], (s, p, "should be [4]"))

    def test_case4(self):
        s = "abcdeabcdeabcde"
        p = "fgh"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [], )

    def test_case5(self):
        s = "aaaaaa"
        p = "aa"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [0, 1, 2, 3, 4],
                         "Should be [0, 1, 2, 3, 4]")

    def test_case6(self):
        s = "abcdefg"
        p = "hij"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [], "Should be []")

    def test_case7(self):
        s = "ababababab"
        p = "abab"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [0, 2, 4, 6], "Should be [0, 2, 4,6]")

    def test_case8(self):
        s = "abcabcabcabc"
        p = "abcabc"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [0, 3, 6], "Should be [0, 3, 6]")

    def test_case9(self):
        s = "abcdefgh"
        p = "gh"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [6], "Should be [6]")

    def test_case10(self):
        s = "ababababab"
        p = "bab"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [1, 3, 5, 7], "Should be [1, 3, 5, 7]")

    def test_case11(self):
        s = "a" * 1000 + "b" * 1000
        p = "b" * 1000
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [1000], "Should be [1000]")

    def test_case12(self):
        s = "PSPdPuuPSPdPddSPuPuudddPddPSdduPdudduPuPSuPuPuPdPSPSdPddPSSdPuSSSdSdudPddduduuSSdudSuuuPduSSPuPudSduuSuuPuuuudPduPPdSuPddPSduPduuuSuuSPdSPuPdSSSPduuPSSdudduSdSduSuPuPPudSdSdSSduuuduSddSSudSdPPuPdudPuSddPPdSudPSuuuuduSSddSSSSSddSduSdPSSSduudSdSuPPPPSuSuuuSdSddudPuPuPSdPuSddPddSudPudPdudPSdSuSuPduPdSSPPPPSPuPSdPuduuuSdPSddPuuuuduPdSSPuPuSSuSuddddPddPPdudPduuPPudSSdSSSSPSddPSPSdSSdPPSuduudPdduSuPudSSduSPSSdSddPPuPSPdSdduuPPduSduuSdPPPudPdPddduSdduSdPdSSdSSSdduuSuSdSSSSPPdSuSuSPSPdPddSPPdPudPuPPddPuSPSuPuSuuuPPuuPdddSuuSduuuSduSSdPuddPPPPPuSSSSdPPSudSdSSudddPPPuSuPSdPPPdSSdPuuPSuduSdSPSduuudSdSuSSSSdPSPuuPSdSdudSPPuduPuuPSuSSdSPduudSdSduduuPSuSSSuuuuSSSuuPuPSuduPdSSududSdddPudSPSuSSudPudPPPddPSPuPPduSduSuuduuuSuPSudPudPduuSSduSuuduPPuSPuuSudSPuSuudPPuSdudSdPPdSSPdPSuddSSuuPSuPuSPudPPSPdPduSdddSPSPuSuuPduuuudSuPSduSSuuSSPSSPuudddudPuSddPdPdPPddudPudPddPduSPPSdPdPuSSSddPPuSPSSSddSdPddPSuPuPuSduSuSPdSSudSPuPPudPPPPPdSPuPSdPuSuuuSdPSSdSPSduPuduPdduSdSSddddudPduSduuPddSddPduPPPSuduuuSddSddudPudSPudPPSSdSuPPuuSdPuSuuPSSdSPPSPduPudSuPPdPPSSSPuPSddudPPduuP"
        p = "PdSu"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [114, 203, 471], "Should be [115,204,472]")

    def test_case13(self):
        s = "HEHHUsUHsEUEsUUUEsUEHUUHUEEsEHHEHHEsEEUEEUEHHEssHEEHsssUsEUsUEHsHUUHUsUsHUsEEEHssEsUHHUsEUHHUUEHHsEEUsEHEHUsHEHEUHHUUEHHHEUHsEHssHsHsUHssEUEHHEHssEUHUHssHHEssssUsHHsEHUHEssUUEUsUUsUUUEsHEHUUHssHssEEUHUHEUHHEUUEHUUEHEUHHssHsssUHEHHHHUHsUHsssHUUUHUsssssUsEEsHsEUHsHUHUEsHsUsEHEHEEHEUEssHUEEEEUUEssHsssHHUHUsEUHHsEsUUUEUEEEHsssHEHEsUHEEsHEUUHUUHsHHHsHUHUEUsHUUEUssHsUEUEUHEsHHUHEEUEHsHEssUsssHHEssHHsHssHHEUHHHHUsUHsHHEHEHHHHHHEssEEUHEUsHsEHsEsUEUsHUEUEEssEHEUUsEHUEUsHsEHEsHHsHsHHUsEUUHHUUEHsHsUsUUUUEEUHsUUHHUHssUHUHUUEHsEUHUEEHEUEHssHEUUHUEUEHHUUUHUHEHEUUHEHUsHEsEEUEUHEHUHUEsssUHUEUHHUHEUEUUUHHsEEssHUHEsEUHHHUHUHEEssUUHsHsHHUHUHEHUUEEUUUUsHEsHsEUssHHEEsHsHsEUEHsHHUHsUUHUEEHsUsUEHsHEsssHsHsHHUHsHsEUHUUsEHHUUUHUHUUEsEHssHUsHEHsHsUUUsEHHHsssEUsUEs"
        p = "sUHE"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [224, 328], "Should be [225,329]")

    def test_case14(self):
        p = "5#9uJm$PxWz@vD(qGkT&eYrV7LtN*HsR2yFgBxM^aQpE8nCwU3KfZc+AbS6Xj"
        s = "5#9uJm$PxWz@vD(qGkT&eYrV7LtNHsR2yFgBxM^aQpE8nCwU3KfZc+AbS6Xj5#9uJm$PxWz@vD(qGkT&eYrV7LtNHsR2yFgBxM^aQpE8nCwU3KfZc+AbS6Xj5#9uJm$PxWz@vD(qGkT&eYrV7LtN*HsR2yFgBxM^aQpE8nCwU3KfZc+AbS6Xj"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [120], "Should be [120]]")

    def test_case15(self):
        p = "abc_123_def_456_ghi_789_abc_123_def_456_ghi_789_abc_123_def_456_ghi_789_abc_123_def_456_ghi_789"
        s = "xyz_555_pqr_888_abc_123_def_456_ghi_789_uvw_111_mno_444_abc_123_def_456_ghi_789_123_789abc_123_def_456_ghi_789_abc_123_def_456_ghi_789_abc_123_def_456_ghi_789_abc_123_def_456_ghi_789"
        index_arr, bad_char, good_suf, match = boyer_moore(s, p)
        self.assertEqual(index_arr, [87], "Should be [87]]")


if __name__ == '__main__':
    unittest.main()
