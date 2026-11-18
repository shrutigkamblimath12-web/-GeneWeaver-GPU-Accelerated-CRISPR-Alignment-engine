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

    st.header("DNA Mutation Analysis")
    st.info("Reference and mutated sequence comparison will be added here.")

# Chromosome Explorer
elif page == "Chromosome Explorer":

    st.header("Chromosome Explorer")
    st.info("Chromosome visualization will be added here.")