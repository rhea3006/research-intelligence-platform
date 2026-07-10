import json
from pgvector.psycopg2 import register_vector
from api.database import get_connection

conn = get_connection()
register_vector(conn)
cursor = conn.cursor()

cursor.execute("""SELECT arxiv_id, embedding FROM papers WHERE embedding IS NOT NULL""")
papers = cursor.fetchall()
print(f"Found {len(papers)} papers")

# ----------------------------
# Migration starts here
# ----------------------------

count = 0

for arxiv_id, embedding_json in papers:
    embedding = json.loads(embedding_json)
    cursor.execute(
        """
        UPDATE papers
        SET embedding_vector = %s
        WHERE arxiv_id = %s
        """,
        (embedding, arxiv_id),
    )

    count += 1

print(f"Migrated {count} embeddings.")

conn.commit()

print("Migration complete!")

cursor.close()
conn.close()