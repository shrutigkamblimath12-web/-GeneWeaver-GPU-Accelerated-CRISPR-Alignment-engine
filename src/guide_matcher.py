# GeneWeaver - CRISPR Guide RNA Matching Engine

from Bio.Seq import Seq

from src.sequence_validator import validate_dna_sequence
from src.crispr_matcher import find_pam_sites


def match_guide_to_targets(guide, target_dna):

    # Normalize input sequences
    guide = "".join(guide.split()).upper()
    target_dna = "".join(target_dna.split()).upper()

    # Validate guide
    valid, message = validate_dna_sequence(guide)

    if not valid:
        raise ValueError(f"Invalid guide: {message}")

    if len(guide) != 20:
        raise ValueError("Guide sequence must contain exactly 20 bases.")

    # Validate target DNA
    valid, message = validate_dna_sequence(target_dna)

    if not valid:
        raise ValueError(f"Invalid target DNA: {message}")

    results = []

    # Search both DNA orientations
    orientations = [
        ("Forward", target_dna),
        ("Reverse", str(Seq(target_dna).reverse_complement()))
    ]

    for strand, oriented_dna in orientations:

        sites = find_pam_sites(oriented_dna)

        for site in sites:

            candidate = site["protospacer"]

            mismatches = []

            # Compare guide with candidate
            for i in range(20):

                if guide[i] != candidate[i]:
                    mismatches.append(i + 1)

            # Convert reverse-strand coordinates
            if strand == "Forward":
                start = site["start"]
                end = site["end"]
            else:
                start = len(target_dna) - site["end"] + 1
                end = len(target_dna) - site["start"] + 1

            results.append({
                "strand": strand,
                "start": start,
                "end": end,
                "target": candidate,
                "pam": site["pam"],
                "mismatch_count": len(mismatches),
                "mismatch_positions": mismatches,
                "identity": ((20 - len(mismatches)) / 20) * 100
            })

    return results


# Test guide matching
if __name__ == "__main__":

    guide = "ATGCGTACGATCGTACGATC"

    target = "ATGCGTACGATCGTACGATCAGG"

    print("\nGENEWEAVER CRISPR GUIDE MATCHING")
    print("--------------------------------")

    print("Guide sequence:", guide)
    print("Target DNA:", target)

    matches = match_guide_to_targets(guide, target)

    if matches:

        print("\nCandidate sites found:", len(matches))

        for result in matches:

            print("\nStrand:", result["strand"])
            print("Position:", result["start"], "-", result["end"])
            print("Target:", result["target"])
            print("PAM:", result["pam"])
            print("Mismatches:", result["mismatch_count"])
            print("Mismatch positions:", result["mismatch_positions"])
            print("Sequence identity:", f"{result['identity']:.2f}%")

    else:
        print("\nNo matching PAM-associated target sites found.")