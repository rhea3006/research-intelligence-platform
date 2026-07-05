from fastapi import FastAPI
from api.models import (PaperSummary, PaperDetail , RelatedPaper, PaperWithRelated, 
                        SearchResult, SemanticSearchResult, SearchResponse)
from api.database import (get_connection, get_all_papers, get_paper_by_id, search_papers,
                           get_related_papers)
from api.services.paper_service import (get_paper_with_related_service,
                                        search_papers_service,get_all_papers_service, 
                                        get_related_papers_service)
'''from api.services.embedding_service import (semantic_search , hybrid_search)'''
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
import requests
from io import BytesIO
import psycopg2


app= FastAPI() #object of FastAPI class, this will represent the entire backend application

app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173",],allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"],)

@app.get("/") # this is root route, whenever the browser visits a particular url, it sends a HTTP request which is get, it tells to run the function below.
def home(): # fastAPI knows whenver we have a GET call, go to home function
    return{"message": "Research Intelligence Platform API"} # FastAPI automatically converts dictionaries into JSON, so it sends it back to the browser.

@app.get("/papers", response_model=list[PaperSummary])
def get_papers(page: int = 1,limit: int = 10):
    return get_all_papers_service(page, limit)

@app.get("/papers/{arxiv_id}",response_model=PaperWithRelated)
def get_paper(arxiv_id):
    return get_paper_with_related_service(arxiv_id)
    

@app.get("/search", response_model=SearchResponse)
def search(q: str, category: str | None = None, author: str | None = None ,year: int | None = None,
           sort: str = "relevance",page: int=1, limit: int=10):
    
    return search_papers_service(q=q, page=page, limit=limit, category=category, author=author,
                                 year=year, sort=sort)

@app.get("/papers/{arxiv_id}/related",response_model=list[RelatedPaper])
def related_papers(arxiv_id: str):
    return get_related_papers_service(arxiv_id)

'''@app.get("/semantic-search")
def semantic_search_endpoint(q: str,response_model=list[SemanticSearchResult]):

    return semantic_search(q)

@app.get("/hybrid-search")
def hybrid_search_endpoint(q: str):
    return hybrid_search(q)'''

@app.get("/papers/{arxiv_id}/download")
def download_paper(arxiv_id: str):
    paper = get_paper_by_id(arxiv_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    pdf_url = paper[7]
    if not pdf_url.endswith(".pdf"):
        pdf_url += ".pdf"

    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return StreamingResponse(
        BytesIO(response.content),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{arxiv_id}.pdf"'},
    )