# GeneWeaver - Pure Python DNA Alignment Engine

from src.sequence_validator import validate_dna_sequence


def perform_alignment(sequence1, sequence2):

    sequence1 = "".join(sequence1.split()).upper()
    sequence2 = "".join(sequence2.split()).upper()

    valid1, message1 = validate_dna_sequence(sequence1)
    valid2, message2 = validate_dna_sequence(sequence2)

    if not valid1:
        raise ValueError(f"Sequence 1: {message1}")

    if not valid2:
        raise ValueError(f"Sequence 2: {message2}")

    match_score = 2
    mismatch_score = -1
    gap_penalty = -2

    m = len(sequence1)
    n = len(sequence2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        dp[i][0] = i * gap_penalty

    for j in range(1, n + 1):
        dp[0][j] = j * gap_penalty

    for i in range(1, m + 1):
        for j in range(1, n + 1):

            diagonal = dp[i-1][j-1] + (
                match_score if sequence1[i-1] == sequence2[j-1]
                else mismatch_score
            )

            up = dp[i-1][j] + gap_penalty
            left = dp[i][j-1] + gap_penalty

            dp[i][j] = max(diagonal, up, left)

    aligned1 = ""
    aligned2 = ""

    i, j = m, n

    while i > 0 or j > 0:

        if i > 0 and j > 0:
            score = match_score if sequence1[i-1] == sequence2[j-1] else mismatch_score

            if dp[i][j] == dp[i-1][j-1] + score:
                aligned1 = sequence1[i-1] + aligned1
                aligned2 = sequence2[j-1] + aligned2
                i -= 1
                j -= 1
                continue

        if i > 0 and dp[i][j] == dp[i-1][j] + gap_penalty:
            aligned1 = sequence1[i-1] + aligned1
            aligned2 = "-" + aligned2
            i -= 1

        else:
            aligned1 = "-" + aligned1
            aligned2 = sequence2[j-1] + aligned2
            j -= 1

    matches = sum(
        a == b and a != "-"
        for a, b in zip(aligned1, aligned2)
    )

    mismatches = sum(
        a != b and a != "-" and b != "-"
        for a, b in zip(aligned1, aligned2)
    )

    gaps = aligned1.count("-") + aligned2.count("-")

    return {
        "aligned_sequence1": aligned1,
        "aligned_sequence2": aligned2,
        "score": dp[m][n],
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps
    }