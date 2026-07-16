def build_prompt(papers, user_prompt):
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

        return f"""
    You are an expert research assistant.

    Use ONLY the information provided below.

    {combined_context}

    User Request:
    {user_prompt}

    Provide a structured response with:

    1. Summary
    2. Comparison
    3. Key Findings
    4. Research Gaps
    5. Final Recommendation
    """

def build_summary_prompt(title: str, abstract: str):
    return f"""
    You are an expert research assistant.

    Summarize the following research paper.

    Return your answer in Markdown.

    Paper Title:
    {title}

    Abstract:
    {abstract}

    Use EXACTLY these headings:

    # Overview

    # Method

    # Key Contributions

    # Results

    # Why It Matters

    Rules:
    - Keep the summary under 300 words.
    - Explain technical concepts clearly.
    - Do not invent information not present in the abstract.
    - Write concise, professional paragraphs.
    """