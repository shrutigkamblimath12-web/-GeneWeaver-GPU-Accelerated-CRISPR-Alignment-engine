import streamlit as st
import plotly.express as px
import pandas as pd
from src.alignment_engine import perform_alignment
# Page configuration
st.set_page_config(
    page_title="GeneWeaver",
    page_icon="🧬",
    layout="wide"
)

# Dashboard heading
st.title("🧬 GeneWeaver")
st.subheader("Advanced Bioinformatics and DNA Sequence Analysis")

st.markdown(
    "An interactive platform for DNA sequence analysis, "
    "alignment, mutation detection and visualization."
)

st.divider()

# Sidebar navigation
st.sidebar.title("GeneWeaver Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "DNA Sequence Analysis",
        "Sequence Visualization",
        "Mutation Analysis",
        "Chromosome Explorer"
    ]
)

# Dashboard
if page == "Dashboard":

    st.header("Welcome to GeneWeaver")

    col1, col2, col3 = st.columns(3)

    col1.metric("Analysis Platform", "Active")
    col2.metric("Sequence Type", "DNA")
    col3.metric("Modules", "5")

    st.info(
        "Enter your DNA sequences in the DNA Sequence Analysis module "
        "to begin analysis."
    )

    st.subheader("Available Features")

    st.markdown("""
    - DNA sequence validation
    - DNA sequence comparison
    - Pairwise sequence alignment
    - CRISPR guide matching
    - Mutation analysis
    - Interactive graphical visualization
    - Chromosome exploration
    """)

# DNA Sequence Analysis
elif page == "DNA Sequence Analysis":

    st.header("DNA Sequence Analysis")

    sequence = st.text_area(
        "Enter DNA Sequence",
        placeholder="Example: ATGCGTACGTAGCTAG",
        height=120
    )

    if st.button("Analyze DNA Sequence"):

        dna = "".join(sequence.upper().split())

        if not dna:
            st.warning("Please enter a DNA sequence.")

        elif any(base not in "ATGC" for base in dna):
            st.error("Invalid DNA sequence. Use only A, T, G and C.")

        else:
            st.success("DNA sequence is valid!")

            a = dna.count("A")
            t = dna.count("T")
            g = dna.count("G")
            c = dna.count("C")

            gc_content = ((g + c) / len(dna)) * 100

            col1, col2, col3 = st.columns(3)

            col1.metric("Sequence Length", len(dna))
            col2.metric("GC Content", f"{gc_content:.2f}%")
            col3.metric("AT Content", f"{100-gc_content:.2f}%")

            st.subheader("Nucleotide Distribution")

            df = pd.DataFrame({
                "Nucleotide": ["A", "T", "G", "C"],
                "Count": [a, t, g, c]
            })

            fig = px.bar(
                df,
                x="Nucleotide",
                y="Count",
                color="Nucleotide",
                title="DNA Nucleotide Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Sequence Preview")
            st.code(dna)

# Sequence Visualization
elif page == "Sequence Visualization":

    st.header("🧬 DNA Sequence Alignment")

    st.write(
        "Compare two DNA sequences using the GeneWeaver "
        "global alignment engine."
    )

    seq1 = st.text_area(
        "Reference DNA Sequence",
        "ATGCGTAC",
        key="reference_sequence"
    )

    seq2 = st.text_area(
        "Query DNA Sequence",
        "ATGACGTAC",
        key="query_sequence"
    )

    if st.button("Perform DNA Alignment"):

        try:
            alignment = perform_alignment(seq1, seq2)

            aligned1 = alignment["aligned_sequence1"]
            aligned2 = alignment["aligned_sequence2"]

            st.success("Alignment completed successfully!")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Alignment Score", alignment["score"])
            col2.metric("Matches", alignment["matches"])
            col3.metric("Mismatches", alignment["mismatches"])
            col4.metric("Gaps", alignment["gaps"])

            st.subheader("Alignment Visualization")

            def color_alignment(a, b):

                if a == "-" or b == "-":
                    color = "#999999"
                elif a == b:
                    color = "#00C853"
                else:
                    color = "#FF5252"

                return (
                    f'<span style="color:{color};'
                    f'font-weight:bold;">{a}</span>'
                )

            html1 = "".join(
                color_alignment(a, b)
                for a, b in zip(aligned1, aligned2)
            )

            html2 = "".join(
                color_alignment(b, a)
                for a, b in zip(aligned1, aligned2)
            )

            st.markdown(
                f"""
                <div style="background-color:#202124;
                            padding:20px;
                            border-radius:10px;
                            font-family:monospace;
                            font-size:18px;
                            overflow-x:auto;">
                    <p style="color:white;">Reference:<br>{html1}</p>
                    <p style="color:white;">Query:<br>{html2}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info("Green = Match | Red = Mismatch | Grey = Gap")

            st.subheader("Complete Alignment Result")

            st.code(
                f"Reference: {aligned1}\n"
                f"Query:     {aligned2}"
            )

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(f"Alignment error: {error}")
# Mutation Analysis
elif page == "Mutation Analysis":

    st.header("🧬 DNA Mutation Analysis")

    st.write(
        "Compare a reference DNA sequence with a mutated "
        "sequence to identify substitutions, insertions and deletions."
    )

    reference = st.text_area(
        "Reference DNA Sequence",
        "ATGCGTAC",
        key="mutation_reference"
    )

    mutated = st.text_area(
        "Mutated DNA Sequence",
        "ATGAGTAC",
        key="mutation_mutated"
    )

    if st.button("Analyze Mutations"):

        ref = "".join(reference.upper().split())
        mut = "".join(mutated.upper().split())

        if not ref or not mut:
            st.warning("Please enter both DNA sequences.")

        elif any(base not in "ATGC" for base in ref + mut):
            st.error("Invalid DNA sequence. Use only A, T, G and C.")

        else:
            try:
                alignment = perform_alignment(ref, mut)

                aligned_ref = alignment["aligned_sequence1"]
                aligned_mut = alignment["aligned_sequence2"]

                substitutions = 0
                insertions = 0
                deletions = 0
                mutation_data = []

                for i, (a, b) in enumerate(
                    zip(aligned_ref, aligned_mut), start=1
                ):

                    if a == b:
                        continue

                    if a == "-":
                        insertions += 1
                        change = "Insertion"

                    elif b == "-":
                        deletions += 1
                        change = "Deletion"

                    else:
                        substitutions += 1
                        change = "Substitution"

                    mutation_data.append({
                        "Alignment Position": i,
                        "Reference": a,
                        "Mutated": b,
                        "Mutation Type": change
                    })

                st.success("Mutation analysis completed!")

                col1, col2, col3 = st.columns(3)

                col1.metric("Substitutions", substitutions)
                col2.metric("Insertions", insertions)
                col3.metric("Deletions", deletions)

                st.metric(
                    "Total Mutations",
                    substitutions + insertions + deletions
                )

                st.subheader("Mutation Comparison")

                st.write("Reference Sequence:")
                st.code(aligned_ref)

                st.write("Mutated Sequence:")
                st.code(aligned_mut)

                st.subheader("Detected Mutations")

                if mutation_data:
                    df = pd.DataFrame(mutation_data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No mutations detected. Both sequences match.")

            except Exception as error:
                st.error(f"Mutation analysis error: {error}")

# Chromosome Explorer
elif page == "Chromosome Explorer":

    st.header("🧬 Interactive Chromosome Explorer")

    st.write(
        "Explore DNA sequence regions and analyze their "
        "nucleotide composition and GC content."
    )

    chromosome = st.selectbox(
        "Select Chromosome",
        [f"Chromosome {i}" for i in range(1, 23)] + [
            "Chromosome X", "Chromosome Y"
        ]
    )

    sequence = st.text_area(
        "Enter DNA Sequence",
        "ATGCGTACGTAGCTAGATCGATCGGCTAATGC",
        key="chromosome_sequence"
    )

    dna = "".join(sequence.upper().split())

    if st.button("Explore Chromosome"):

        if not dna:
            st.warning("Please enter a DNA sequence.")

        elif any(base not in "ATGC" for base in dna):
            st.error("Invalid DNA sequence. Use only A, T, G and C.")

        else:
            st.success(f"Exploring {chromosome}!")

            col1, col2, col3 = st.columns(3)

            col1.metric("Sequence Length", len(dna))
            col2.metric("A + T", dna.count("A") + dna.count("T"))
            col3.metric("G + C", dna.count("G") + dna.count("C"))

            st.subheader("Chromosome Sequence Overview")

            st.write(
                f"Selected region: 1 to {len(dna)}"
            )

            st.progress(
                1.0,
                text="DNA sequence loaded successfully"
            )

            st.subheader("GC Content Analysis")

            window_size = st.selectbox(
                "Select Analysis Window Size",
                [4, 8, 10, 16],
                index=1,
                key="chromosome_window"
            )

            if len(dna) < window_size:
                st.warning(
                    "DNA sequence is shorter than the selected window."
                )

            else:
                positions = []
                gc_values = []

                for start in range(
                    0, len(dna) - window_size + 1, window_size
                ):
                    window = dna[start:start + window_size]

                    gc = (
                        (window.count("G") + window.count("C"))
                        / len(window)
                    ) * 100

                    positions.append(start + 1)
                    gc_values.append(gc)

                df = pd.DataFrame({
                    "Starting Position": positions,
                    "GC Content (%)": gc_values
                })

                fig = px.line(
                    df,
                    x="Starting Position",
                    y="GC Content (%)",
                    markers=True,
                    title="GC Content Across DNA Regions"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader("Region Analysis Results")

                st.dataframe(
                    df,
                    use_container_width=True
                )
                st.subheader("📥 Download Analysis Reports")
csv_data = df.to_csv(index=False)

st.download_button(
    "Download GC Analysis (CSV)",
    data=csv_data,
    file_name="geneweaver_gc_analysis.csv",
    mime="text/csv"
)

fasta_data = f">{chromosome}_DNA_Sequence\n{dna}\n"

st.download_button(
    "Download DNA Sequence (FASTA)",
    data=fasta_data,
    file_name="geneweaver_sequence.fasta",
    mime="text/plain"
)

st.subheader("DNA Sequence")

st.code(dna)