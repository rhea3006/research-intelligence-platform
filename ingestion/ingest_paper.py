import requests
import feedparser
import psycopg2
from api.database import get_connection
from pgvector.psycopg2 import register_vector
from api.services.embedding_service import create_paper_embedding


def fetch_papers(query, max_results):
    url = "https://export.arxiv.org/api/query"
    params = {"search_query": query,"start": 0,"max_results": max_results,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    response = requests.get(url, params=params)
    feed = feedparser.parse(response.text)
    return feed.entries

def extract_paper_data(paper):
    return {"arxiv_id": paper.id.split("/")[-1],
            "title": paper.title,
            "abstract": paper.summary,
            "authors":", ".join(author.name for author in paper.authors),
            "categories":", ".join(tag.term for tag in paper.tags),
            "arxiv_url":next((link.href for link in paper.links if "pdf" in link.href),None),
            "published_date":paper.published[:10],"updated_date":paper.updated[:10]
            }


def save_paper(cursor, paper_data):
    cursor.execute("""INSERT INTO papers(arxiv_id, title, abstract, authors, categories, 
        arxiv_url, published_date, updated_date,embedding_vector)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (arxiv_id)
        DO NOTHING""",
        (
            paper_data["arxiv_id"],
            paper_data["title"],
            paper_data["abstract"],
            paper_data["authors"],
            paper_data["categories"],
            paper_data["arxiv_url"],
            paper_data["published_date"],
            paper_data["updated_date"],
            paper_data["embedding_vector"]

        )
    )
    return cursor.rowcount

def run_ingestion(query="all:machine learning", max_results=150, verbose=True,):
    conn = get_connection()
    cursor = conn.cursor()
    papers = fetch_papers(query=query,max_results=max_results,)
    inserted_count = 0
    skipped_count = 0

    for paper in papers:
        paper_data = extract_paper_data(paper)
        paper_data["embedding_vector"] = create_paper_embedding(
            paper_data["title"],
            paper_data["abstract"],
        )
        inserted = save_paper(cursor, paper_data)
        if verbose:
            if inserted:
                print(f"Inserted: {paper_data['title']}")
            else:
                print(f"Skipped: {paper_data['title']}")

        if inserted:
            inserted_count += 1
        else:
            skipped_count += 1 

    if verbose:
        print(f"Inserted: {inserted_count}")
        print(f"Skipped: {skipped_count}")
    conn.commit()
    

    cursor.close()
    conn.close()

    return {
        "inserted": inserted_count,
        "skipped": skipped_count,
    }

def main():
    run_ingestion()


if __name__ == "__main__":
    main()