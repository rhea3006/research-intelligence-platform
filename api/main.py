from fastapi import FastAPI
from api.models import PaperSummary 
from api.models import PaperDetail
from api.models import SearchResult
from api.models import RelatedPaper
from api.database import get_connection
from api.database import get_all_papers
from api.database import get_paper_by_id
from api.database import search_papers
from api.database import get_related_papers
import psycopg2


app= FastAPI() #object of FastAPI class, this will represent the entire backend application

@app.get("/") # this is root route, whenever the browser visits a particular url, it sends a HTTP request which is get, it tells to run the function below.
def home(): # fastAPI knows whenver we have a GET call, go to home function
    return{"message": "Research Intelligence Platform API"} # FastAPI automatically converts dictionaries into JSON, so it sends it back to the browser.

@app.get("/papers", response_model=list[PaperSummary])
def get_papers(page: int = 1,limit: int = 10):

    offset = (page - 1) * limit
    results= get_all_papers(limit,offset)
    papers = []
    for row in results:
        papers.append({ "arxiv_id": row[0],"title": row[1]})

    return papers

@app.get("/papers/{arxiv_id}",response_model=PaperDetail)
def get_paper(arxiv_id):

    paper=get_paper_by_id(arxiv_id)
    
    return {"arxiv_id": paper[1],"title": paper[2],"abstract": paper[3],
            "published_date": str(paper[4]) if paper[4] else None,
            "authors":paper[5], "categories":paper[6],"arxiv_url": paper[7],}

@app.get("/search", response_model=list[SearchResult])
def search(q: str,page: int=1, limit: int=10):
    offset= (page - 1)* limit
    
    results= search_papers(q,limit, offset)
    papers=[]
    for row in results:
        papers.append({"arxiv_id":row[0], "title": row[1],"authors": row[2],
                       "published_date": str(row[3]) if row[3] else None, "relevance_score": row[4] })

    
    return papers

@app.get("/papers/{arxiv_id}/related",response_model=list[RelatedPaper])
def related_papers(arxiv_id: str):
    results = get_related_papers(arxiv_id)

    papers = []

    for row in results:
        papers.append({
            "arxiv_id": row[0],
            "title": row[1],
            "authors": row[2],
            "published_date": row[3],
            "similarity_score": row[4]
        })

    return papers
