import requests
import feedparser
import psycopg2
from api.database import get_connection,paper_exists
from pgvector.psycopg2 import register_vector
from api.services.embedding_service import create_paper_embedding


def fetch_papers(query,start=0,max_results=100,sort_by="submittedDate",sort_order="descending",):
    url = "https://export.arxiv.org/api/query"

    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }

    response = requests.get(url,params=params,timeout=30,)

    response.raise_for_status()

    feed = feedparser.parse(response.text)

    print(f"Query: {query}")
    print(f"Start: {start}")
    print(f"Returned entries: {len(feed.entries)}")

    if hasattr(feed, "feed"):
        print("OpenSearch totalResults:", feed.feed.get("opensearch_totalresults"))

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

def run_ingestion(
    query="all:machine learning",
    max_results=20,
    verbose=True,
):
    conn = get_connection()
    cursor = conn.cursor()

    inserted_count = 0
    skipped_count = 0

    try:
        papers = fetch_papers(
            query=query,
            max_results=max_results,
        )

        for paper in papers:
            paper_data = extract_paper_data(paper)

            if paper_exists(cursor, paper_data["arxiv_id"]):
                skipped_count += 1

                if verbose:
                    print(f"Skipped: {paper_data['title']}")

                continue

            paper_data["embedding_vector"] = create_paper_embedding(
                paper_data["title"],
                paper_data["abstract"],
            )

            inserted = save_paper(cursor, paper_data)
            inserted_count += inserted

        conn.commit()

        return {
            "inserted": inserted_count,
            "skipped": skipped_count,
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def main():
    stats= run_ingestion(verbose=True)
    print(
        f"✅ Ingestion complete | "
        f"Inserted: {stats['inserted']} | "
        f"Skipped: {stats['skipped']}"
    )


if __name__ == "__main__":
    main()