import unittest

from src.alignment_engine import perform_alignment


class TestAlignmentEngine(unittest.TestCase):

    def test_valid_alignment(self):
        result = perform_alignment("ATGCGTAC", "ATGACGTAC")
        self.assertIsNotNone(result)
        self.assertEqual(result.score, 14.0)

    def test_identical_sequences(self):
        result = perform_alignment("ATGC", "ATGC")
        self.assertEqual(result.score, 8.0)

    def test_lowercase_sequences(self):
        result = perform_alignment("atgc", "ATGC")
        self.assertEqual(result.score, 8.0)

    def test_invalid_sequence(self):
        with self.assertRaises(ValueError):
            perform_alignment("ATGX", "ATGC")

    def test_empty_sequence(self):
        with self.assertRaises(ValueError):
            perform_alignment("", "ATGC")


if __name__ == "__main__":
    unittest.main()