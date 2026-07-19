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

def build_summary_prompt(title: str, abstract: str) -> str:
    return f"""
You are an expert AI research assistant helping researchers quickly evaluate academic papers.

Your task is to analyze the following paper and produce a structured research brief.

The response MUST be written in Markdown.

Use the following headings exactly.

# Executive Summary

Provide a concise overview of the paper in 2–3 paragraphs.

---

# Key Contributions

List 3–5 major contributions as bullet points.

---

# Methodology

Explain:
- The approach used
- Models or techniques employed
- Dataset (if mentioned)
- Evaluation strategy

---

# Main Findings

Summarize the most important results and conclusions.

---

# Practical Applications

List real-world applications of this research.

If not explicitly mentioned, infer reasonable applications based on the paper.

---

# Limitations

Mention limitations, assumptions, or potential weaknesses.

If none are explicitly stated, infer likely limitations based on the methodology.

---

# Future Research Directions

Suggest future work based on the paper.

If the paper already mentions future work, include it.

Otherwise infer logical research directions.

---

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