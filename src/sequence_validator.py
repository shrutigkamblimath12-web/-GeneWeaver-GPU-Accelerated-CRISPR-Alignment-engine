# GeneWeaver - DNA Sequence Validator

VALID_BASES = set("ATGC")


def validate_dna_sequence(sequence):

    # Check input type
    if not isinstance(sequence, str):
        return False, "DNA sequence must be a string."

    # Convert to uppercase and remove spaces
    sequence = "".join(sequence.split()).upper()

    # Check empty sequence
    if not sequence:
        return False, "DNA sequence cannot be empty."

    # Find invalid DNA bases
    invalid_bases = set(sequence) - VALID_BASES

    if invalid_bases:
        invalid = ", ".join(sorted(invalid_bases))
        return False, f"Invalid DNA bases found: {invalid}"

    return True, "Valid DNA sequence."


# Test the DNA sequence validator
if __name__ == "__main__":

    test_sequences = [
        "ATGCGTAC",
        "ATGXGTAC",
        "ATGCATGC",
        "",
        "atgc",
        "ATG C G T",
        123
    ]

    for dna in test_sequences:
        valid, message = validate_dna_sequence(dna)

        print("\nDNA Sequence:", dna)
        print("Status:", message)