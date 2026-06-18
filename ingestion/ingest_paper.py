import requests
import feedparser
import psycopg2

def fetch_papers(query, max_results):
    url = "https://export.arxiv.org/api/query"
    params = {"search_query": query,"start": 0,"max_results": max_results}
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
            "published_date":paper.published[:10]
            }

def save_paper(cursor, paper_data):
    cursor.execute("""INSERT INTO papers(arxiv_id, title, abstract, authors, categories, arxiv_url, published_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (arxiv_id)
        DO NOTHING""",
        (
            paper_data["arxiv_id"],
            paper_data["title"],
            paper_data["abstract"],
            paper_data["authors"],
            paper_data["categories"],
            paper_data["arxiv_url"],
            paper_data["published_date"]
        )
    )

def main():
    conn = psycopg2.connect(dbname="research_intelligence",user="rheamathur",host="localhost")
    cursor = conn.cursor()
    papers = fetch_papers( query="all:machine learning", max_results=10)
    for paper in papers:
        paper_data = extract_paper_data(paper)
        save_paper(cursor,paper_data)
        
        print(f"Processed: {paper_data['title']}")

    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()