import unittest

from src.sequence_validator import validate_dna_sequence


class TestDNAValidator(unittest.TestCase):

    def test_valid_dna_sequence(self):
        self.assertEqual(
            validate_dna_sequence("ATGC"),
            (True, "Valid DNA sequence.")
        )

    def test_invalid_dna_sequence(self):
        valid, message = validate_dna_sequence("ATGX")

        self.assertFalse(valid)
        self.assertIn("X", message)

    def test_lowercase_sequence(self):
        self.assertTrue(
            validate_dna_sequence("atgc")[0]
        )

    def test_sequence_with_spaces(self):
        self.assertTrue(
            validate_dna_sequence("ATG C G T")[0]
        )

    def test_empty_sequence(self):
        self.assertFalse(
            validate_dna_sequence("")[0]
        )

    def test_non_string_input(self):
        self.assertEqual(
            validate_dna_sequence(123),
            (False, "DNA sequence must be a string.")
        )

    def test_multiple_invalid_bases(self):
        valid, message = validate_dna_sequence("ATGXZ")

        self.assertFalse(valid)
        self.assertIn("X, Z", message)


if __name__ == "__main__":
    unittest.main()