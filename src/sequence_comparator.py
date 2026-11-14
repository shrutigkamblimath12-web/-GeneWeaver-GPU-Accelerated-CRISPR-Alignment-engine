# GeneWeaver - DNA Sequence Comparison Engine

from src.sequence_validator import validate_dna_sequence


def compare_sequences(sequence1, sequence2):

    # Normalize both sequences
    sequence1 = "".join(sequence1.split()).upper()
    sequence2 = "".join(sequence2.split()).upper()

    # Validate sequences
    valid1, message1 = validate_dna_sequence(sequence1)
    valid2, message2 = validate_dna_sequence(sequence2)

    if not valid1:
        raise ValueError(f"Sequence 1: {message1}")

    if not valid2:
        raise ValueError(f"Sequence 2: {message2}")

    # This first version compares equal-length sequences
    if len(sequence1) != len(sequence2):
        raise ValueError("Both sequences must have equal lengths.")

    matches = 0
    mismatches = []

    # Compare each position
    for i in range(len(sequence1)):

        if sequence1[i] == sequence2[i]:
            matches += 1
        else:
            mismatches.append({
                "position": i + 1,
                "base1": sequence1[i],
                "base2": sequence2[i]
            })

    total = len(sequence1)

    identity = (matches / total) * 100

    return {
        "total_positions": total,
        "matches": matches,
        "mismatches": len(mismatches),
        "mismatch_details": mismatches,
        "identity": identity
    }


# Test the comparison engine
if __name__ == "__main__":

    seq1 = "ATGCGTAC"
    seq2 = "ATGAGTTC"

    result = compare_sequences(seq1, seq2)

    print("\nGENEWEAVER DNA SEQUENCE ANALYSIS")
    print("--------------------------------")
    print("Sequence 1:", seq1)
    print("Sequence 2:", seq2)

    print("\nTotal positions:", result["total_positions"])
    print("Matching positions:", result["matches"])
    print("Mismatches:", result["mismatches"])

    print("\nMismatch details:")

    for item in result["mismatch_details"]:
        print(
            f"Position {item['position']}: "
            f"{item['base1']} -> {item['base2']}"
        )

    print(
        "\nSequence Identity:",
        f"{result['identity']:.2f}%"
    )