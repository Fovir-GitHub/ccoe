import unittest
from src.ccoe_ai.normalization.phone import normalize_phone


class TestNormalizePhone(unittest.TestCase):
    def test_valid_number(self):
        self.assertEqual(normalize_phone("0123456789", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("12-3456789", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("+60123456789", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("+6012 3456789", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("+6012-3456789", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("+60012-3456789", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("+60012-34567 8 9", "MY"), "+60123456789")
        self.assertEqual(normalize_phone("+60012-3 4567 8 9   ", "MY"), "+60123456789")
        self.assertEqual(
            normalize_phone("+60012---3 4567 8 9   ", "MY"), "+60123456789"
        )

    def test_invalid_number(self):
        INVALID_NUMBER = "N/A"
        self.assertEqual(normalize_phone("", "MY"), INVALID_NUMBER)
        self.assertEqual(normalize_phone("012345678910", "MY"), INVALID_NUMBER)
        self.assertEqual(normalize_phone("0123456789abc", "MY"), INVALID_NUMBER)
        self.assertEqual(normalize_phone("abc", "MY"), INVALID_NUMBER)
        self.assertEqual(normalize_phone("0123456789", ""), INVALID_NUMBER)
        self.assertEqual(normalize_phone("0123456789 abc", ""), INVALID_NUMBER)


if __name__ == "__main__":
    unittest.main()
