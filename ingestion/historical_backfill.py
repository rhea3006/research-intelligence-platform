from api.database import get_connection, paper_exists
from ingestion.ingest_paper import (fetch_papers,extract_paper_data,save_paper,)
from api.services.embedding_service import create_paper_embedding

TARGET_PAPERS = 5000
BATCH_SIZE = 100

CATEGORIES = [
    "cs.AI",
    "cs.LG",
    "stat.ML",
    "cs.CL",
    "cs.CV",
    "cs.CR",
    "cs.RO",
    "cs.IR",   # Information Retrieval
    "cs.SE",   # Software Engineering
    "cs.DB",   # Databases
    "cs.DC",   # Distributed Computing
    "cs.NE",   # Neural & Evolutionary Computing
    "cs.HC",   # Human-Computer Interaction
    "cs.CY",   # Cybersecurity
]

def run_backfill():
    conn = get_connection()
    cursor = conn.cursor()

    inserted_total = 0
    for category in CATEGORIES:
        print("=" * 60)
        print(f"Category: {category}")
        print("=" * 60)

        start = 0
        while inserted_total < TARGET_PAPERS:
            papers = fetch_papers(query=f"cat:{category}",start=start,max_results=BATCH_SIZE,
                                  sort_by="submittedDate",sort_order="ascending",)
            if not papers:
                print("No more papers in this category.")
                break

            for paper in papers:
                paper_data = extract_paper_data(paper)
                if paper_exists(cursor, paper_data["arxiv_id"]):
                    print(f"Skipped: {paper_data['title']}")
                    continue
                paper_data["embedding_vector"] = create_paper_embedding(paper_data["title"],
                                                                        paper_data["abstract"],)
                inserted = save_paper(cursor, paper_data)
                if inserted:
                    inserted_total += 1
                    print(f"[{inserted_total}/{TARGET_PAPERS}] "
                          f"Inserted: {paper_data['title']}")
                    if inserted_total >= TARGET_PAPERS:
                        conn.commit()
                        break

            if inserted_total >= TARGET_PAPERS:
                break

            conn.commit()
            start += BATCH_SIZE

        if inserted_total >= TARGET_PAPERS:
            break

    conn.commit()
    cursor.close()
    conn.close()

    print("=" * 60)
    print(f"Historical backfill complete.")
    print(f"Inserted {inserted_total} papers.")
    print("=" * 60)


def main():
    run_backfill()


if __name__ == "__main__":
    main()



