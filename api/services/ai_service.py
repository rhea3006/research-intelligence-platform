def build_prompt(papers,analysis_type,additional_prompt,analysis_depth,
                 writing_style,output_format,):
    """
    Construct the prompt that will be sent to the LLM.
    """

    paper_context = []

    for index, paper in enumerate(papers, start=1):
        paper_context.append(
            f"""
    Paper {index}

    Title:
    {paper.title}

    Authors:
    {paper.authors}

    Categories:
    {paper.categories}

    Abstract:
    {paper.abstract}
    """
        )

    combined_context = "\n".join(paper_context)

    if analysis_type == "methodology":
        analysis_instruction = """
        Generate a structured methodology analysis.

        Include:
        1. Research Objectives
        2. Datasets and Experimental Setup
        3. Models and Algorithms Used
        4. Evaluation Metrics
        5. Methodological Strengths and Weaknesses
        6. Comparative Summary
        """

    elif analysis_type == "literature_review":
        analysis_instruction = """
        Generate a structured literature review.

        Include:
        1. Research Theme
        2. Existing Work
        3. Major Trends
        4. Open Problems
        5. Conclusion
        """

    elif analysis_type == "critical_evaluation":
        analysis_instruction = """
        Generate a critical evaluation of the selected papers.

        Include:
        1. Key Strengths
        2. Major Limitations
        3. Assumptions and Potential Biases
        4. Threats to Validity
        5. Reproducibility and Practical Feasibility
        6. Overall Assessment
        """

    elif analysis_type == "applications":
        analysis_instruction = """
        Generate an analysis of the practical applications of the selected papers.

        Include:
        1. Potential Industry Applications
        2. Real-World Use Cases
        3. Benefits and Impact
        4. Implementation Challenges
        5. Future Commercial Opportunities
        6. Overall Practical Relevance
        """
    return f"""
        You are an expert research assistant.

        Use ONLY the information provided below.

        ==========================
        PAPERS
        ==========================

        {combined_context}

        ==========================
        TASK
        ==========================

        {analysis_instruction}

        ==========================
        USER PREFERENCES
        ==========================

        Additional Instructions:
        {additional_prompt or "None"}

        Analysis Depth:
        {analysis_depth}

        Writing Style:
        {writing_style}

        Output Format:
        {output_format}

        Do not invent facts that are not supported by the provided papers.
        """

    
def build_summary_prompt(title: str, abstract: str) -> str:
    return f"""
    You are an expert AI research assistant helping researchers quickly evaluate academic papers.

    Your task is to analyze the following paper and produce a structured research brief.

    The response MUST be written in Markdown.

    Use the following headings exactly.

    # Executive Summary

    Provide a concise overview of the paper in 2–3 paragraphs.


    # Key Contributions

    List 3–5 major contributions as bullet points.


    # Methodology

    Explain:
    - The approach used
    - Models or techniques employed
    - Dataset (if mentioned)
    - Evaluation strategy


    # Main Findings

    Summarize the most important results and conclusions.


    # Practical Applications

    List real-world applications of this research.

    If not explicitly mentioned, infer reasonable applications based on the paper.


    # Limitations

    Mention limitations, assumptions, or potential weaknesses.

    If none are explicitly stated, infer likely limitations based on the methodology.


    # Future Research Directions

    Suggest future work based on the paper.

    If the paper already mentions future work, include it.

    Otherwise infer logical research directions.


    Paper Title:
    {title}

    Abstract:
    {abstract}


    Guidelines:

    - Keep the response under 700 words.
    - Be objective and factual.
    - Do not invent claims unsupported by the abstract.
    - When information is missing, clearly state that it is not specified rather than guessing.
    - Use concise bullet points wherever appropriate.
    - Do not repeat information across sections.
    """