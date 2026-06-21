import streamlit as st

from src.rag import ask_rag

from src.features import (
    generate_project_ideas,
    recommend_tech_stack,
    generate_roadmap,
    generate_architecture,
    generate_elevator_pitch,
    generate_judge_questions
)

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Hackathon AI Assistant",
    page_icon="🚀",
    layout="wide"
)

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    st.title("🚀 Hackathon AI Assistant")

    st.markdown("---")

    st.markdown("""
### Your AI companion for hackathons

#### Features

💡 Project Ideas

⚙️ Tech Stack Recommendations

🏗️ System Architecture

🗺️ Development Roadmaps

🎤 Elevator Pitches

🧑‍⚖️ Judge Preparation

🔍 Knowledge Assistant
""")

# ==================================
# HEADER
# ==================================

st.title("🚀 Hackathon AI Assistant")

st.markdown("""
Transform ideas into hackathon-ready projects.

Generate innovative project ideas, recommend technology stacks,
design system architectures, create development roadmaps,
craft elevator pitches, and prepare for judge questions —
all from a single platform.
""")

st.markdown("---")

# ==================================
# TABS
# ==================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💡 Project Ideas",
    "⚙️ Tech Stack",
    "🗺️ Roadmap",
    "🏗️ Architecture",
    "🎤 Elevator Pitch",
    "🧑‍⚖️ Judge Questions",
    "🔍 Ask Anything"
])

# ==================================
# PROJECT IDEAS
# ==================================

with tab1:

    st.subheader("Generate Project Ideas")

    domain = st.text_input(
        "Domain",
        placeholder="Healthcare, Agriculture, Education..."
    )

    if st.button("Generate Ideas"):

        if not domain.strip():

            st.warning("Please enter a domain.")

        else:

            with st.spinner("Generating ideas..."):

                result = generate_project_ideas(domain)

                st.markdown(result["answer"])

# ==================================
# TECH STACK
# ==================================

with tab2:

    st.subheader("Recommend Technology Stack")

    project = st.text_area(
        "Project Description",
        key="tech"
    )

    if st.button("Recommend Tech Stack"):

        if not project.strip():

            st.warning("Please enter a project description.")

        else:

            with st.spinner("Analyzing project..."):

                result = recommend_tech_stack(project)

                st.markdown(result["answer"])

# ==================================
# ROADMAP
# ==================================

with tab3:

    st.subheader("Generate Development Roadmap")

    project = st.text_area(
        "Project Description",
        key="roadmap"
    )

    if st.button("Generate Roadmap"):

        if not project.strip():

            st.warning("Please enter a project description.")

        else:

            with st.spinner("Generating roadmap..."):

                result = generate_roadmap(project)

                st.markdown(result["answer"])

# ==================================
# ARCHITECTURE
# ==================================

with tab4:

    st.subheader("Generate System Architecture")

    project = st.text_area(
        "Project Description",
        key="architecture"
    )

    if st.button("Generate Architecture"):

        if not project.strip():

            st.warning("Please enter a project description.")

        else:

            with st.spinner("Designing architecture..."):

                result = generate_architecture(project)

                st.markdown(result["answer"])

# ==================================
# ELEVATOR PITCH
# ==================================

with tab5:

    st.subheader("Generate Elevator Pitch")

    project = st.text_area(
        "Project Description",
        key="pitch"
    )

    if st.button("Generate Pitch"):

        if not project.strip():

            st.warning("Please enter a project description.")

        else:

            with st.spinner("Generating pitch..."):

                result = generate_elevator_pitch(project)

                st.markdown(result["answer"])

# ==================================
# JUDGE QUESTIONS
# ==================================

with tab6:

    st.subheader("Generate Judge Questions")

    project = st.text_area(
        "Project Description",
        key="judge"
    )

    if st.button("Generate Questions"):

        if not project.strip():

            st.warning("Please enter a project description.")

        else:

            with st.spinner("Generating questions..."):

                result = generate_judge_questions(project)

                st.markdown(result["answer"])

# ==================================
# ASK ANYTHING
# ==================================

with tab7:

    st.subheader("Ask Your Knowledge Base")

    question = st.text_input(
        "Question"
    )

    if st.button("Ask"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching..."):

                result = ask_rag(question)

                st.markdown(result["answer"])

                with st.expander("📚 Sources"):

                    for source in result["sources"]:
                        st.write(source)