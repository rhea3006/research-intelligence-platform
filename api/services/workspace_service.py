from api.services.llm_service import llm
from api.database import (get_workspace_papers,get_paper_by_id)
from api.models import (WorkspaceAnalysisRequest,WorkspaceAnalysisResponse,WorkspacePaper,)
from api.services.ai_service import (build_prompt,build_summary_prompt)


def analyze_workspace_service(request: WorkspaceAnalysisRequest,):
    papers = get_workspace_papers(request.paper_ids)
    workspace_papers = []

    for paper in papers:
        workspace_papers.append(
            WorkspacePaper(
                arxiv_id=paper[0],
                title=paper[1],
                abstract=paper[2],
                authors=paper[3],
                categories=paper[4],
                published_date=str(paper[5]) if paper[5] else None,
            )
        )
    
    prompt = build_prompt(
        papers=workspace_papers,
        analysis_type=request.analysis_type,
        additional_prompt=request.additional_prompt,
        analysis_depth=request.analysis_depth,
        writing_style=request.writing_style,
        output_format=request.output_format,
    )
    
    try:
        analysis = llm.generate_response(prompt)

    except Exception as e:
        raise RuntimeError(
            f"Failed to generate workspace analysis: {e}"
        )

    return WorkspaceAnalysisResponse(analysis=analysis,)

def summarize_paper_service(arxiv_id: str):
    paper = get_paper_by_id(arxiv_id)

    if not paper:
        raise ValueError("Paper not found")
    
    title = paper[2]
    abstract = paper[3] 
    prompt = build_summary_prompt(title, abstract)
    summary = llm.generate_response(prompt)

    return {"arxiv_id": arxiv_id, "title": title, "summary": summary,}