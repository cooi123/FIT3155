import unittest
from bitwisepm import bitwisepm


class TestCases(unittest.TestCase):
    def test_case1(self):
        s = "acxcbbacababacabaaaabacabaafacababacaba"
        p = "acababacaba"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [6, 28], "Should be [6, 28]")

    def test_case2(self):
        s = "ababcababcabcabc"
        p = "abcabc"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [7, 10], (s, p))

    def test_case3(self):
        s = "mississippi"
        p = "issip"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [4], (s, p, "should be [4]"))

    def test_case4(self):
        s = "abcdeabcdeabcde"
        p = "fgh"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [], )

    def test_case5(self):
        s = "aaaaaa"
        p = "aa"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [0, 1, 2, 3, 4],
                         "Should be [0, 1, 2, 3, 4]")

    def test_case6(self):
        s = "abcdefg"
        p = "hij"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [], "Should be []")

    def test_case7(self):
        s = "ababababab"
        p = "abab"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [0, 2, 4, 6], "Should be [0, 2, 4,6]")

    def test_case8(self):
        s = "abcabcabcabc"
        p = "abcabc"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [0, 3, 6], "Should be [0, 3, 6]")

    def test_case9(self):
        s = "abcdefgh"
        p = "gh"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [6], "Should be [6]")

    def test_case10(self):
        s = "ababababab"
        p = "bab"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [1, 3, 5, 7], "Should be [1, 3, 5, 7]")

    def test_case11(self):
        s = "a" * 1000 + "b" * 1000
        p = "b" * 1000
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [1000], "Should be [1000]")

    def test_case12(self):
        s = "ababababab"
        p = "ababababab"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [0], "Should be [0]")

    def test_case13(self):
        s = "ababababab"
        p = "abababababa"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [], "Should be []")

    def test_case14(self):
        s = "abcdefgabcdefgabcdefg"
        p = "def"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [3, 10, 17], "Should be [3,10,17]")

    def test_case15(self):
        s = "mississippimississippi"
        p = "issi"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr, [1, 4, 12, 15], "Should be [1,4,12,15]")

    def test_case16(self):
        s = "CkbkCkCkbbbkbCbbkCCbkCkkbCbkCCkCbkkkkbkCCkCkCbCkCbkbCbbbCbkCCbCCbCkkbkCkkkkkbkCbkkbCbCbbbkCkCCkCkbCbkCkbkbkCCCCCCbbCkbkCkkbbbCCbbkkkCbCbCkCCbbkCCkbkbbkbbbbkbkbbbCbCCbkkkbbbCbbkkkkbCCCCkCkbCCbCCCbCkbCCbbCbCCCkkbkCkkkCkCbkCCCCbkCkCbkCkbCbkkbCkCkbbbCCbCCbkCkCCbkCbkkCCbkbbCCCbkCbkbCkCCCbbCbkbkbbCbCkbCbkkCCCkbkbkCkCkkCbkbkCCCbbkCkCbkbCbCbCkCkkbCbkCbkkkbCCkCbkCbkCkbCCCCbbbCCbbkkbbCkCbkkCkCbkCbkkkkkkbbkbbkCCbCCCbCbkbkkbkkkbbkbkkkCkbkbkbCCbCbCbbbCCCCbbbbCkkCbCbbkCbbbCkkCkkbCkkCkkbkbbbCkkkkkCkkkkbCCbCkbCbkCCCkkCkkbkCkkkCkbbk"
        p = "bkC"
        index_arr = bitwisepm(s, p)
        arr = [3, 25, 49, 63, 118, 132, 136, 158, 199, 212, 216, 223, 234, 254, 265, 273, 285, 296, 302,
               314, 338, 406, 415, 421, 426, 448, 454, 469, 504, 514, 520, 539, 551, 554, 583, 597, 654, 697, 707]
        self.assertEqual(index_arr, arr, "Should be [1,4,12,15]")

    def test_case17(self):
        s = "PSPdPuuPSPdPddSPuPuudddPddPSdduPdudduPuPSuPuPuPdPSPSdPddPSSdPuSSSdSdudPddduduuSSdudSuuuPduSSPuPudSduuSuuPuuuudPduPPdSuPddPSduPduuuSuuSPdSPuPdSSSPduuPSSdudduSdSduSuPuPPudSdSdSSduuuduSddSSudSdPPuPdudPuSddPPdSudPSuuuuduSSddSSSSSddSduSdPSSSduudSdSuPPPPSuSuuuSdSddudPuPuPSdPuSddPddSudPudPdudPSdSuSuPduPdSSPPPPSPuPSdPuduuuSdPSddPuuuuduPdSSPuPuSSuSuddddPddPPdudPduuPPudSSdSSSSPSddPSPSdSSdPPSuduudPdduSuPudSSduSPSSdSddPPuPSPdSdduuPPduSduuSdPPPudPdPddduSdduSdPdSSdSSSdduuSuSdSSSSPPdSuSuSPSPdPddSPPdPudPuPPddPuSPSuPuSuuuPPuuPdddSuuSduuuSduSSdPuddPPPPPuSSSSdPPSudSdSSudddPPPuSuPSdPPPdSSdPuuPSuduSdSPSduuudSdSuSSSSdPSPuuPSdSdudSPPuduPuuPSuSSdSPduudSdSduduuPSuSSSuuuuSSSuuPuPSuduPdSSududSdddPudSPSuSSudPudPPPddPSPuPPduSduSuuduuuSuPSudPudPduuSSduSuuduPPuSPuuSudSPuSuudPPuSdudSdPPdSSPdPSuddSSuuPSuPuSPudPPSPdPduSdddSPSPuSuuPduuuudSuPSduSSuuSSPSSPuudddudPuSddPdPdPPddudPudPddPduSPPSdPdPuSSSddPPuSPSSSddSdPddPSuPuPuSduSuSPdSSudSPuPPudPPPPPdSPuPSdPuSuuuSdPSSdSPSduPuduPdduSdSSddddudPduSduuPddSddPduPPPSuduuuSddSddudPudSPudPPSSdSuPPuuSdPuSuuPSSdSPPSPduPudSuPPdPPSSSPuPSddudPPduuP"
        p = "PdSu"
        index_arr = bitwisepm(s, p)
        self.assertEqual(index_arr,  [115, 204, 472])


if __name__ == '__main__':
    unittest.main()
