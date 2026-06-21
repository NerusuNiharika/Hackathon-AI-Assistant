from src.rag import ask_rag


def generate_project_ideas(domain):

    query = f"""
    Generate 5 innovative hackathon project ideas for {domain}.

    For each idea provide:
    - Problem
    - Solution
    - Innovation
    - Expected Impact
    """

    return ask_rag(query)


def recommend_tech_stack(project):

    query = f"""
    Recommend the best technology stack for:

    {project}

    Include:
    - Frontend
    - Backend
    - Database
    - AI/ML Tools
    - Deployment
    - APIs
    """

    return ask_rag(query)


def generate_roadmap(project):

    query = f"""
    Create a hackathon development roadmap for:

    {project}

    Include:
    - Planning
    - Development
    - Testing
    - Deployment
    - Presentation Preparation

    Give a timeline.
    """

    return ask_rag(query)


def generate_architecture(project):

    query = f"""
    Design a complete system architecture for:

    {project}

    Include:
    - Components
    - User Flow
    - Database Flow
    - APIs
    - AI Components
    - Deployment Architecture

    Explain clearly.
    """

    return ask_rag(query)


def generate_elevator_pitch(project):

    query = f"""
    Generate a 45-second elevator pitch for:

    {project}

    Include:
    - Problem
    - Solution
    - Impact
    - Closing Statement
    """

    return ask_rag(query)


def generate_judge_questions(project):

    query = f"""
    Generate 15 hackathon judge questions for:

    {project}

    Also provide strong answers for each question.
    """

    return ask_rag(query)