# GeneWeaver - DNA Sequence Validator

VALID_BASES = set("ATGC")


def validate_dna_sequence(sequence):

    # Convert to uppercase and remove spaces
    sequence = "".join(sequence.split()).upper()

    # Check empty sequence
    if not sequence:
        return False, "DNA sequence cannot be empty."

    # Find invalid DNA bases
    invalid_bases = set(sequence) - VALID_BASES

    if invalid_bases:
        return False, f"Invalid DNA bases found: {invalid_bases}"

    return True, "Valid DNA sequence."


# Test the DNA sequence validator
if __name__ == "__main__":

    test_sequences = [
        "ATGCGTAC",
        "ATGXGTAC",
        "ATGCATGC",
        ""
    ]

    for dna in test_sequences:
        valid, message = validate_dna_sequence(dna)

        print("\nDNA Sequence:", dna)
        print("Status:", message)