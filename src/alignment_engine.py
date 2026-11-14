# GeneWeaver - Advanced DNA Sequence Alignment Engine

from Bio.Align import PairwiseAligner
from src.sequence_validator import validate_dna_sequence


def perform_alignment(sequence1, sequence2):

    # Normalize DNA sequences
    sequence1 = "".join(sequence1.split()).upper()
    sequence2 = "".join(sequence2.split()).upper()

    # Validate both sequences
    valid1, message1 = validate_dna_sequence(sequence1)
    valid2, message2 = validate_dna_sequence(sequence2)

    if not valid1:
        raise ValueError(f"Sequence 1: {message1}")

    if not valid2:
        raise ValueError(f"Sequence 2: {message2}")

    # Configure the alignment algorithm
    aligner = PairwiseAligner()

    # Global alignment
    aligner.mode = "global"

    # Alignment scoring
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -0.5

    # Perform alignment
    alignments = aligner.align(sequence1, sequence2)

    if len(alignments) == 0:
        raise ValueError("No alignment found.")

    # Select the best alignment
    best_alignment = alignments[0]

    return best_alignment


# Test the alignment engine
if __name__ == "__main__":

    seq1 = "ATGCGTAC"
    seq2 = "ATGACGTAC"

    result = perform_alignment(seq1, seq2)

    print("\nGENEWEAVER ADVANCED DNA ALIGNMENT")
    print("---------------------------------")

    print("Sequence 1:", seq1)
    print("Sequence 2:", seq2)

    print("\nAlignment Result:")
    print(result)

    print("Alignment Score:", result.score)