from api.database import (
    get_chunks_for_embedding,
    update_chunk_embedding,
)
from clients.embedding_client import generate_embedding


ARXIV_ID = "2607.08374v1"


def embed_paper_chunks(arxiv_id):
    chunks = get_chunks_for_embedding(arxiv_id=arxiv_id)

    print(f"🔎 Found {len(chunks)} unembedded chunks.")

    if not chunks:
        print("✅ All chunks are already embedded.")
        return

    successful = 0
    failed = 0

    for position, chunk in enumerate(chunks, start=1):
        chunk_id, paper_id, chunk_index, text = chunk

        print(
            f"\n🧠 Embedding chunk "
            f"{position}/{len(chunks)} "
            f"(chunk_index={chunk_index})"
        )

        try:
            embedding = generate_embedding(text)

            if len(embedding) != 384:
                raise ValueError(
                    f"Expected 384 dimensions, "
                    f"got {len(embedding)}"
                )

            update_chunk_embedding(
                chunk_id=chunk_id,
                embedding=embedding,
            )

            successful += 1

            print(
                f"✅ Chunk {chunk_index} embedded successfully."
            )

        except Exception as e:
            failed += 1

            print(
                f"❌ Chunk {chunk_index} failed: {e}"
            )

    print("\n" + "=" * 60)
    print("📊 EMBEDDING SUMMARY")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Failed:     {failed}")
    print(f"Total:      {len(chunks)}")


if __name__ == "__main__":
    embed_paper_chunks(ARXIV_ID)