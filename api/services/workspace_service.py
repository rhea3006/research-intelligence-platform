from api.database import get_workspace_papers
from api.models import (WorkspaceAnalysisRequest,WorkspaceAnalysisResponse,WorkspacePaper,)
from api.services.ai_service import build_prompt


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
    
    prompt = build_prompt(workspace_papers,request.prompt,)
    print(prompt)

    return WorkspaceAnalysisResponse(
        papers=workspace_papers,
        prompt=request.prompt,
    )