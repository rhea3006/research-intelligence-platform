from api.services.retrieval_service import retrieve_chunks


QUERY = "How does the proposed method improve personality recognition?"

ARXIV_ID = "2607.08374v1"


print("🔎 Query:")
print(QUERY)

print("\n🧠 Searching relevant chunks...")

results = retrieve_chunks(
    query=QUERY,
    limit=5,
    arxiv_id=ARXIV_ID,
)

print(f"\nFound {len(results)} chunks.\n")

for rank, result in enumerate(results, start=1):

    print("=" * 70)
    print(f"Rank: {rank}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Chunk index: {result['chunk_index']}")
    print(f"Section: {result['section']}")
    print(f"Similarity: {result['similarity']:.4f}")

    print("\nText:")
    print(result["text"][:800])