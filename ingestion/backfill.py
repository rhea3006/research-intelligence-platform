from insert_paper import get_connection
from ingest_paper import fetch_papers

def get_papers_missing_updated_date(cursor):
    cursor.execute("""SELECT arxiv_id FROM papers WHERE updated_date IS NULL""")

    return cursor.fetchall()

def fetch_paper_by_id(arxiv_id):
    papers = fetch_papers(query=f"id:{arxiv_id}", max_results=1)

    if papers:
        return papers[0]

    return None

def update_updated_date(cursor, arxiv_id, updated_date):
    cursor.execute("""UPDATE papers SET updated_date = %s WHERE arxiv_id = %s""",
                    (updated_date, arxiv_id))

def backfill_updated_dates():

    conn = get_connection()
    cursor = conn.cursor()

    missing_papers = get_papers_missing_updated_date(cursor)
    print(f"Found {len(missing_papers)} papers")

    for paper in missing_papers:
        arxiv_id = paper[0]
        fetched_paper = fetch_paper_by_id(arxiv_id)
        if fetched_paper:
            updated_date = fetched_paper.updated[:10]
            update_updated_date(cursor, arxiv_id, updated_date)
            print(f"Updated {arxiv_id}")

    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    backfill_updated_dates()