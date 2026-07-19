from api.database import search_papers


def search_papers_service(q, page, limit, category=None, author=None, year=None,sort="relevance"):
    offset= (page - 1)* limit
    
    results, total = search_papers(q,limit,offset,category,author,year,sort,)
    papers=[]

    for row in results:
        papers.append({
            "arxiv_id": row[0],
            "title": row[1],
            "abstract": row[2],
            "authors": row[3],
            "categories": row[4],
            "published_date": str(row[5]) if row[5] else None,
            "relevance_score": row[6],
            "embedding": row[7],
        })
    

    return {
        "results": papers,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total + limit - 1) // limit,
    }