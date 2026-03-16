import unittest
from src.ccoe_ai.normalization.country import normalize_country


class TestNormalizeCountry(unittest.TestCase):
    def test_valid_country(self):
        self.assertEqual(normalize_country("MY"), "MY")
        self.assertEqual(normalize_country("sg"), "SG")

    def test_invalid_country(self):
        DEFAULT_COUNTRY = "MY"
        self.assertEqual(normalize_country(""), DEFAULT_COUNTRY)
        self.assertEqual(normalize_country("XX"), DEFAULT_COUNTRY)


if __name__ == "__main__":
    unittest.main()
