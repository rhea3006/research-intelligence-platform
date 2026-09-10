from api.database import (
    get_chunks_for_embedding,
    update_chunk_embedding,
    get_connection,
)
from clients.embedding_client import generate_embedding


ARXIV_ID = "2607.08374v1"


print("🔎 Finding an unembedded chunk...")

chunks = get_chunks_for_embedding(arxiv_id=ARXIV_ID)

if not chunks:
    print("⚠️ No unembedded chunks found.")
    raise SystemExit

chunk_id, arxiv_id, chunk_index, text = chunks[0]

print(f"Paper: {arxiv_id}")
print(f"Chunk index: {chunk_index}")
print(f"Chunk ID: {chunk_id}")
print(f"Text length: {len(text)}")


print("\n🧠 Generating embedding...")

embedding = generate_embedding(text)

print(f"Embedding dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")


if len(embedding) != 384:
    raise ValueError(
        f"Expected 384 dimensions, got {len(embedding)}"
    )


print("\n💾 Saving embedding...")

update_chunk_embedding(
    chunk_id=chunk_id,
    embedding=embedding,
)

print("✅ Embedding saved.")


print("\n🔍 Verifying database...")

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        id,
        chunk_index,
        embedding_vector IS NOT NULL,
        vector_dims(embedding_vector)
    FROM paper_chunks
    WHERE id = %s
    """,
    (chunk_id,),
)

row = cursor.fetchone()

cursor.close()
conn.close()

print(f"Database result: {row}")

if row[2] and row[3] == 384:
    print("\n🎉 Chunk embedding verification successful!")
else:
    print("\n❌ Embedding verification failed.")