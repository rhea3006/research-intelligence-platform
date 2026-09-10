from api.database import get_connection


ARXIV_ID = "2607.08374v1"


conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        COUNT(*) AS total_chunks,
        COUNT(embedding_vector) AS embedded_chunks,
        COUNT(*) - COUNT(embedding_vector) AS missing_embeddings
    FROM paper_chunks
    WHERE arxiv_id = %s
    """,
    (ARXIV_ID,),
)

total, embedded, missing = cursor.fetchone()

print("=" * 50)
print("📊 CHUNK EMBEDDING VERIFICATION")
print("=" * 50)
print(f"Total chunks:       {total}")
print(f"Embedded chunks:    {embedded}")
print(f"Missing embeddings: {missing}")

cursor.execute(
    """
    SELECT
        MIN(vector_dims(embedding_vector)),
        MAX(vector_dims(embedding_vector))
    FROM paper_chunks
    WHERE arxiv_id = %s
      AND embedding_vector IS NOT NULL
    """,
    (ARXIV_ID,),
)

min_dims, max_dims = cursor.fetchone()

print(f"Minimum dimensions: {min_dims}")
print(f"Maximum dimensions: {max_dims}")

cursor.close()
conn.close()


if (
    total == 35
    and embedded == 35
    and missing == 0
    and min_dims == 384
    and max_dims == 384
):
    print("\n🎉 All chunk embeddings verified successfully!")
else:
    print("\n❌ Verification failed.")