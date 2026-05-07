"""Streamlit app for an interactive computational biology cell atlas.

Run locally with:
    streamlit run app.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import plotly.graph_objects as go
import streamlit as st


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[str, ...]
    answer: str
    explanation: str


@dataclass(frozen=True)
class CellProfile:
    name: str
    kingdom: str
    summary: str
    theory: tuple[str, ...]
    labels: tuple[str, ...]
    quiz: tuple[QuizQuestion, ...]
    color: str
    shape: str


STUDENT_DETAILS = {
    "Name": "Ummarvali muzakir",
    "Registration number": "RA2511026050021",
    "Department": "CSE Aiml",
    "Section": "A",
}

CELL_PROFILES: tuple[CellProfile, ...] = (
    CellProfile(
        name="Animal Cell",
        kingdom="Eukaryotic",
        summary="A flexible membrane-bound eukaryotic cell that performs specialized functions in animals.",
        theory=(
            "Animal cells contain a nucleus, mitochondria, endoplasmic reticulum, Golgi body, lysosomes, ribosomes, and a plasma membrane.",
            "Computational biology models animal cells to understand gene expression, cancer growth, tissue engineering, and drug response.",
            "Unlike plant cells, animal cells do not have a rigid cell wall or chloroplasts, which allows many shapes and movement patterns.",
        ),
        labels=("Plasma membrane", "Nucleus", "Mitochondria", "Golgi body", "Rough ER", "Lysosome", "Ribosomes"),
        quiz=(
            QuizQuestion(
                "Which organelle is the main site of ATP production in animal cells?",
                ("Nucleus", "Mitochondria", "Golgi body", "Lysosome"),
                "Mitochondria",
                "Mitochondria perform aerobic respiration and produce most cellular ATP.",
            ),
            QuizQuestion(
                "Which structure controls movement of substances into and out of an animal cell?",
                ("Plasma membrane", "Cell wall", "Chloroplast", "Vacuole"),
                "Plasma membrane",
                "The selectively permeable plasma membrane regulates transport.",
            ),
        ),
        color="#7dd3fc",
        shape="sphere",
    ),
    CellProfile(
        name="Plant Cell",
        kingdom="Eukaryotic",
        summary="A photosynthetic eukaryotic cell with a cell wall, chloroplasts, and a large central vacuole.",
        theory=(
            "Plant cells convert light energy into chemical energy using chloroplasts and support the plant body with cellulose-rich cell walls.",
            "The large central vacuole stores water and solutes, maintains turgor pressure, and contributes to plant rigidity.",
            "Computational models of plant cells help predict photosynthesis, crop yield, stress responses, and gene regulation.",
        ),
        labels=("Cell wall", "Plasma membrane", "Nucleus", "Chloroplast", "Central vacuole", "Mitochondria", "Golgi body"),
        quiz=(
            QuizQuestion(
                "Which plant cell organelle carries out photosynthesis?",
                ("Mitochondrion", "Chloroplast", "Nucleus", "Ribosome"),
                "Chloroplast",
                "Chloroplasts contain chlorophyll and convert light energy into sugars.",
            ),
            QuizQuestion(
                "What is a major function of the central vacuole?",
                ("Protein synthesis", "Turgor pressure", "DNA replication", "Flagellar motion"),
                "Turgor pressure",
                "The central vacuole stores water and helps keep plant tissues firm.",
            ),
        ),
        color="#86efac",
        shape="box",
    ),
    CellProfile(
        name="Bacterial Cell",
        kingdom="Prokaryotic",
        summary="A small prokaryotic cell without a membrane-bound nucleus, often protected by a cell wall.",
        theory=(
            "Bacterial cells contain a nucleoid region, plasmids, ribosomes, cytoplasm, a plasma membrane, and usually a peptidoglycan cell wall.",
            "Some bacteria have capsules, pili, or flagella that help with protection, attachment, and movement.",
            "Computational biology is used to analyze bacterial genomes, antibiotic resistance, microbiomes, and infection spread.",
        ),
        labels=("Capsule", "Cell wall", "Plasma membrane", "Nucleoid DNA", "Plasmid", "Ribosomes", "Flagellum"),
        quiz=(
            QuizQuestion(
                "Where is bacterial genetic material mainly found?",
                ("Nucleoid", "Nucleus", "Chloroplast", "Vacuole"),
                "Nucleoid",
                "Bacteria do not have a membrane-bound nucleus; DNA is concentrated in the nucleoid.",
            ),
            QuizQuestion(
                "Which structure commonly helps bacteria move?",
                ("Flagellum", "Chloroplast", "Golgi body", "Central vacuole"),
                "Flagellum",
                "A flagellum rotates or waves to propel many bacterial cells.",
            ),
        ),
        color="#fbbf24",
        shape="rod",
    ),
    CellProfile(
        name="Fungal Cell",
        kingdom="Eukaryotic",
        summary="A eukaryotic cell with a chitin-rich cell wall; examples include yeast and mold cells.",
        theory=(
            "Fungal cells have nuclei, mitochondria, vacuoles, ribosomes, membranes, and cell walls made mainly of chitin and glucans.",
            "Yeast cells are single-celled fungi, while many fungi grow as thread-like hyphae that form mycelium.",
            "Computational biology supports fungal genome annotation, antifungal drug discovery, fermentation design, and ecosystem studies.",
        ),
        labels=("Chitin cell wall", "Plasma membrane", "Nucleus", "Vacuole", "Mitochondria", "ER", "Ribosomes"),
        quiz=(
            QuizQuestion(
                "What major polymer strengthens fungal cell walls?",
                ("Cellulose", "Chitin", "Peptidoglycan", "Keratin"),
                "Chitin",
                "Fungal cell walls are rich in chitin, unlike plant walls that are rich in cellulose.",
            ),
            QuizQuestion(
                "Fungal cells are classified as which cell type?",
                ("Prokaryotic", "Eukaryotic", "Acellular", "Viral"),
                "Eukaryotic",
                "Fungal cells contain membrane-bound nuclei and organelles.",
            ),
        ),
        color="#c084fc",
        shape="sphere",
    ),
    CellProfile(
        name="Protist Cell",
        kingdom="Eukaryotic",
        summary="A diverse eukaryotic cell type found in algae, amoebae, and protozoans.",
        theory=(
            "Protists may be photosynthetic, heterotrophic, or mixotrophic, and many live in aquatic or moist environments.",
            "Common structures include nucleus, mitochondria, contractile vacuoles, cilia, flagella, pseudopodia, and sometimes chloroplasts.",
            "Computational biology helps compare protist genomes, trace evolution, monitor harmful algal blooms, and study parasites.",
        ),
        labels=("Cell membrane", "Nucleus", "Contractile vacuole", "Mitochondria", "Cilia/flagellum", "Food vacuole", "Cytoplasm"),
        quiz=(
            QuizQuestion(
                "Which structure helps many freshwater protists remove excess water?",
                ("Contractile vacuole", "Cell wall", "Nucleoid", "Capsule"),
                "Contractile vacuole",
                "Contractile vacuoles pump out excess water to maintain osmotic balance.",
            ),
            QuizQuestion(
                "Protists are best described as what?",
                ("Only bacteria", "Diverse eukaryotes", "Only viruses", "Only animal tissues"),
                "Diverse eukaryotes",
                "Protists include many unrelated eukaryotic lineages.",
            ),
        ),
        color="#fb7185",
        shape="sphere",
    ),
    CellProfile(
        name="Neuron",
        kingdom="Specialized animal cell",
        summary="A nerve cell specialized for electrical and chemical communication.",
        theory=(
            "Neurons contain a cell body, nucleus, dendrites, axon, synaptic terminals, mitochondria, and sometimes myelin insulation.",
            "They receive signals through dendrites, process information in the cell body, and transmit impulses along the axon.",
            "Computational neuroscience uses mathematical models to simulate neuron firing, neural circuits, learning, and brain disorders.",
        ),
        labels=("Dendrites", "Cell body", "Nucleus", "Axon", "Myelin sheath", "Synaptic terminals", "Mitochondria"),
        quiz=(
            QuizQuestion(
                "Which neuron part usually carries signals away from the cell body?",
                ("Axon", "Dendrite", "Nucleus", "Ribosome"),
                "Axon",
                "The axon transmits action potentials away from the soma toward terminals.",
            ),
            QuizQuestion(
                "What is a key role of myelin?",
                ("Slow signaling", "Speed signal conduction", "Digest proteins", "Store DNA"),
                "Speed signal conduction",
                "Myelin electrically insulates axons and increases conduction speed.",
            ),
        ),
        color="#60a5fa",
        shape="neuron",
    ),
    CellProfile(
        name="Red Blood Cell",
        kingdom="Specialized animal cell",
        summary="A biconcave blood cell specialized for transporting oxygen with hemoglobin.",
        theory=(
            "Mature human red blood cells lack a nucleus and most organelles, creating more space for hemoglobin.",
            "Their biconcave shape increases surface area for gas exchange and helps them squeeze through capillaries.",
            "Computational models can study oxygen transport, blood flow, anemia, malaria, and cell deformability.",
        ),
        labels=("Biconcave membrane", "Hemoglobin-rich cytoplasm", "Flexible cytoskeleton", "No nucleus", "Oxygen binding area"),
        quiz=(
            QuizQuestion(
                "What molecule allows red blood cells to carry oxygen?",
                ("Hemoglobin", "Chlorophyll", "Collagen", "Insulin"),
                "Hemoglobin",
                "Hemoglobin binds oxygen in the lungs and releases it in tissues.",
            ),
            QuizQuestion(
                "Mature human red blood cells usually lack which structure?",
                ("Nucleus", "Membrane", "Cytoplasm", "Hemoglobin"),
                "Nucleus",
                "Human RBCs eject the nucleus during maturation.",
            ),
        ),
        color="#ef4444",
        shape="disc",
    ),
    CellProfile(
        name="White Blood Cell",
        kingdom="Specialized animal cell",
        summary="An immune cell that identifies, attacks, or coordinates defenses against pathogens.",
        theory=(
            "White blood cells include lymphocytes, neutrophils, monocytes, eosinophils, and basophils, each with distinct immune roles.",
            "They can engulf pathogens, produce antibodies, release signaling molecules, and remember previous infections.",
            "Computational immunology predicts immune-cell behavior, vaccine response, inflammation, and immunotherapy outcomes.",
        ),
        labels=("Cell membrane", "Lobed nucleus", "Granules", "Cytoplasm", "Receptors", "Lysosomes", "Mitochondria"),
        quiz=(
            QuizQuestion(
                "Which body system uses white blood cells as key defenders?",
                ("Immune system", "Skeletal system", "Digestive system", "Integumentary system"),
                "Immune system",
                "White blood cells are central components of immune defense.",
            ),
            QuizQuestion(
                "Which white blood cell type can produce antibodies after activation?",
                ("B lymphocyte", "Red blood cell", "Platelet", "Neuron"),
                "B lymphocyte",
                "Activated B cells can become plasma cells that secrete antibodies.",
            ),
        ),
        color="#f8fafc",
        shape="sphere",
    ),
)


def sphere_mesh(radius: float = 1.0, rows: int = 34, cols: int = 34) -> tuple[list[float], list[float], list[float]]:
    x: list[float] = []
    y: list[float] = []
    z: list[float] = []
    for i in range(rows):
        theta = math.pi * i / (rows - 1)
        for j in range(cols):
            phi = 2 * math.pi * j / (cols - 1)
            x.append(radius * math.sin(theta) * math.cos(phi))
            y.append(radius * math.sin(theta) * math.sin(phi))
            z.append(radius * math.cos(theta))
    return x, y, z


def add_surface(fig: go.Figure, name: str, color: str, radius: float, opacity: float = 0.45) -> None:
    x, y, z = sphere_mesh(radius)
    fig.add_trace(
        go.Mesh3d(
            x=x,
            y=y,
            z=z,
            alphahull=0,
            color=color,
            opacity=opacity,
            name=name,
            hoverinfo="name",
        )
    )


def add_marker(fig: go.Figure, label: str, xyz: tuple[float, float, float], color: str = "#111827", size: int = 5) -> None:
    fig.add_trace(
        go.Scatter3d(
            x=[xyz[0]],
            y=[xyz[1]],
            z=[xyz[2]],
            mode="markers+text",
            marker={"size": size, "color": color},
            text=[label],
            textposition="top center",
            name=label,
            hovertext=label,
            hoverinfo="text",
        )
    )


def add_label_ring(fig: go.Figure, labels: Iterable[str], radius: float = 1.42) -> None:
    labels = tuple(labels)
    for index, label in enumerate(labels):
        angle = 2 * math.pi * index / max(len(labels), 1)
        add_marker(fig, label, (radius * math.cos(angle), radius * math.sin(angle), 0.34 * math.sin(angle * 2)))


def build_cell_figure(profile: CellProfile) -> go.Figure:
    fig = go.Figure()

    if profile.shape == "box":
        fig.add_trace(
            go.Mesh3d(
                x=[-1.15, 1.15, 1.15, -1.15, -1.15, 1.15, 1.15, -1.15],
                y=[-0.85, -0.85, 0.85, 0.85, -0.85, -0.85, 0.85, 0.85],
                z=[-0.65, -0.65, -0.65, -0.65, 0.65, 0.65, 0.65, 0.65],
                i=[0, 0, 0, 1, 4, 4, 2, 3, 0, 1, 5, 6],
                j=[1, 2, 3, 5, 5, 6, 6, 7, 4, 5, 6, 7],
                k=[2, 3, 7, 6, 6, 7, 7, 4, 5, 6, 7, 4],
                color=profile.color,
                opacity=0.38,
                name="Cell wall / body",
            )
        )
    elif profile.shape == "rod":
        x, y, z = sphere_mesh(0.72)
        fig.add_trace(
            go.Mesh3d(
                x=[value * 1.9 for value in x],
                y=[value * 0.72 for value in y],
                z=[value * 0.72 for value in z],
                alphahull=0,
                color=profile.color,
                opacity=0.46,
                name="Rod-shaped cell body",
            )
        )
        fig.add_trace(
            go.Scatter3d(
                x=[1.35, 1.75, 2.1, 2.45],
                y=[0.0, 0.1, -0.05, 0.15],
                z=[0.0, 0.28, -0.16, 0.08],
                mode="lines",
                line={"color": "#374151", "width": 8},
                name="Flagellum",
            )
        )
    elif profile.shape == "disc":
        x, y, z = sphere_mesh(1.0)
        fig.add_trace(
            go.Mesh3d(
                x=x,
                y=y,
                z=[0.28 * value - 0.18 * math.exp(-(x[idx] ** 2 + y[idx] ** 2) * 2) for idx, value in enumerate(z)],
                alphahull=0,
                color=profile.color,
                opacity=0.62,
                name="Biconcave disc",
            )
        )
    elif profile.shape == "neuron":
        add_surface(fig, "Cell body", profile.color, 0.72, 0.5)
        for angle in (0, math.pi / 3, 2 * math.pi / 3, math.pi, 4 * math.pi / 3):
            fig.add_trace(
                go.Scatter3d(
                    x=[0.35 * math.cos(angle), 1.2 * math.cos(angle)],
                    y=[0.35 * math.sin(angle), 1.2 * math.sin(angle)],
                    z=[0, 0.3 * math.sin(angle)],
                    mode="lines",
                    line={"color": profile.color, "width": 10},
                    name="Dendrite",
                )
            )
        fig.add_trace(
            go.Scatter3d(
                x=[0.65, 1.4, 2.25, 3.0],
                y=[0, -0.05, 0.06, 0],
                z=[0, 0.02, -0.02, 0.03],
                mode="lines",
                line={"color": "#2563eb", "width": 12},
                name="Axon",
            )
        )
    else:
        add_surface(fig, "Cell membrane / body", profile.color, 1.0, 0.42)

    add_surface(fig, "Nucleus or DNA region", "#818cf8", 0.32, 0.72)
    add_marker(fig, "Nucleus / DNA", (0.0, 0.0, 0.48), "#312e81", 6)
    add_marker(fig, "Mitochondrion", (-0.55, 0.42, -0.12), "#dc2626", 5)
    add_marker(fig, "Golgi / vesicles", (0.58, -0.36, 0.08), "#9333ea", 5)
    add_marker(fig, "Ribosomes", (-0.34, -0.48, 0.22), "#0f172a", 4)
    add_label_ring(fig, profile.labels)

    fig.update_layout(
        height=560,
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        scene={
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False},
            "aspectmode": "data",
        },
        showlegend=False,
        title={"text": f"3D labelled model: {profile.name}", "x": 0.5},
    )
    return fig


def render_student_card() -> None:
    details_html = "".join(f"<b>{key}:</b> {value}<br>" for key, value in STUDENT_DETAILS.items())
    st.sidebar.markdown(
        f"""
        <div class="student-card">
            <h3>Student Details</h3>
            {details_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quiz(profile: CellProfile) -> None:
    st.subheader(f"Quiz for {profile.name}")
    score = 0
    for index, question in enumerate(profile.quiz, start=1):
        response = st.radio(
            question.question,
            question.options,
            key=f"{profile.name}-{index}",
            index=None,
        )
        if response:
            if response == question.answer:
                score += 1
                st.success(f"Correct. {question.explanation}")
            else:
                st.error(f"Incorrect. Correct answer: {question.answer}. {question.explanation}")
    st.info(f"Current score for this cell: {score}/{len(profile.quiz)}")


def main() -> None:
    st.set_page_config(
        page_title="Introduction of Computational Biology",
        page_icon="🧬",
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .main-title {font-size: 3rem; font-weight: 800; color: #0f766e;}
        .subtitle {font-size: 1.1rem; color: #334155;}
        .student-card {position: sticky; top: 1rem; padding: 1rem; border-radius: 1rem; background: linear-gradient(135deg, #ecfeff, #f0fdf4); border: 1px solid #99f6e4; box-shadow: 0 6px 18px rgba(15, 118, 110, 0.14);}
        .cell-chip {display: inline-block; padding: .25rem .65rem; border-radius: 999px; background: #e0f2fe; color: #075985; font-weight: 700; margin-bottom: .5rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    render_student_card()

    st.markdown('<div class="main-title">Introduction of Computational Biology</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">A public Streamlit learning website with biological cell theory, interactive 3D labelled models, and quizzes for students.</p>',
        unsafe_allow_html=True,
    )

    st.write(
        "Computational biology combines biology, computer science, mathematics, and statistics to analyze living systems. "
        "This app presents representative biological cells and explains how computational methods help study their structure, function, and data."
    )

    selected_name = st.sidebar.selectbox("Choose a biological cell", [profile.name for profile in CELL_PROFILES])
    profile = next(cell for cell in CELL_PROFILES if cell.name == selected_name)

    left, right = st.columns([1.25, 1])
    with left:
        st.plotly_chart(build_cell_figure(profile), use_container_width=True)
    with right:
        st.markdown(f'<span class="cell-chip">{profile.kingdom}</span>', unsafe_allow_html=True)
        st.header(profile.name)
        st.write(profile.summary)
        st.subheader("Theory")
        for point in profile.theory:
            st.markdown(f"- {point}")
        st.subheader("Labels included")
        st.write(", ".join(profile.labels))

    st.divider()
    render_quiz(profile)

    st.divider()
    st.header("Complete cell theory overview")
    tabs = st.tabs([profile.name for profile in CELL_PROFILES])
    for tab, cell in zip(tabs, CELL_PROFILES, strict=True):
        with tab:
            st.subheader(cell.name)
            st.write(cell.summary)
            for point in cell.theory:
                st.markdown(f"- {point}")
            st.caption("Quiz is available by selecting this cell from the sidebar.")


if __name__ == "__main__":
    main()
