from api.database import get_paper_by_id, get_related_papers, search_papers, get_all_papers

def get_paper_with_related_service(arxiv_id):
    paper=get_paper_by_id(arxiv_id)
    
    paper_data= {"arxiv_id": paper[1],"title": paper[2],"abstract": paper[3],
            "published_date": str(paper[4]) if paper[4] else None,
            "authors":paper[5], "categories":paper[6],"arxiv_url": paper[7],
            "updated_date": paper[8]}
    
    related= get_related_papers(arxiv_id)
    related_papers = []

    for row in related:
        related_papers.append({"arxiv_id": row[0], "title": row[1], "authors": row[2],
            "published_date": row[3],"similarity_score": row[4]})

    return {"paper": paper_data, "related_papers": related_papers}

def search_papers_service(q, page, limit, category=None, author=None, year=None):
    offset= (page - 1)* limit
    
    results= search_papers(q,limit, offset, category, author,year)
    papers=[]
    for row in results:
        papers.append({"arxiv_id":row[0], "title": row[1],"authors": row[2],
                       "published_date": str(row[3]) if row[3] else None, "relevance_score": row[4] })

    
    return papers

def get_all_papers_service(page, limit):
    offset = (page - 1) * limit
    results= get_all_papers(limit,offset)
    papers = []
    for row in results:
        papers.append({ "arxiv_id": row[0],"title": row[1]})

    return papers

def get_related_papers_service(arxiv_id):
    results = get_related_papers(arxiv_id)

    papers = []

    for row in results:
        papers.append({
            "arxiv_id": row[0],
            "title": row[1],
            "authors": row[2],
            "published_date": row[3],
            "similarity_score": row[4]})

    return papers