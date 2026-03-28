import unittest
from src.ccoe_ai.normalization.country import normalize_country


class TestNormalizeCountry(unittest.TestCase):
    def test_valid_country(self):
        self.assertEqual(normalize_country("MY"), "MY")
        self.assertEqual(normalize_country("sg"), "SG")
        self.assertEqual(normalize_country("Singapore"), "SG")
        self.assertEqual(normalize_country("Malaysia"), "MY")
        self.assertEqual(normalize_country("Singapore "), "SG")
        self.assertEqual(normalize_country(" Singapore "), "SG")
        self.assertEqual(normalize_country("United States"), "US")
        self.assertEqual(normalize_country("United   States"), "US")
        self.assertEqual(normalize_country("USA"), "US")
        self.assertEqual(normalize_country("Taiwan, Province of China"), "TW")
        self.assertEqual(normalize_country("Taiwan, Province   of   China"), "TW")
        self.assertEqual(normalize_country("Taiwan"), "TW")
        self.assertEqual(normalize_country("UK"), "GB")
        self.assertEqual(normalize_country("America"), "US")

    def test_invalid_country(self):
        DEFAULT_COUNTRY = "MY"
        self.assertEqual(normalize_country(""), DEFAULT_COUNTRY)
        self.assertEqual(normalize_country("XX"), DEFAULT_COUNTRY)
        self.assertEqual(normalize_country("?"), DEFAULT_COUNTRY)
        self.assertEqual(normalize_country("Sgapore"), DEFAULT_COUNTRY)


if __name__ == "__main__":
    unittest.main()
