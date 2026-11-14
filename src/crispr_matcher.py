# GeneWeaver - CRISPR PAM Detection

from src.sequence_validator import validate_dna_sequence


def find_pam_sites(sequence):

    # Normalize DNA sequence
    sequence = "".join(sequence.split()).upper()

    # Validate sequence
    valid, message = validate_dna_sequence(sequence)

    if not valid:
        raise ValueError(message)

    results = []

    # Scan for a 20-base region followed by NGG
    for i in range(len(sequence) - 22):

        protospacer = sequence[i:i + 20]
        pam = sequence[i + 20:i + 23]

        # PAM pattern: N can be any DNA base, followed by GG
        if pam[1:] == "GG":

            results.append({
                "start": i + 1,
                "end": i + 23,
                "protospacer": protospacer,
                "pam": pam
            })

    return results


# Test PAM detection
if __name__ == "__main__":

    dna_sequence = "ATGCGTACGATCGTACGATCAGG"

    print("\nGENEWEAVER CRISPR PAM DETECTOR")
    print("--------------------------------")

    print("Input DNA:", dna_sequence)

    sites = find_pam_sites(dna_sequence)

    if sites:

        print("\nPAM sites found:", len(sites))

        for site in sites:

            print("\nTarget region:", site["protospacer"])
            print("PAM sequence:", site["pam"])
            print("Start position:", site["start"])
            print("End position:", site["end"])

    else:
        print("\nNo PAM sites found.")