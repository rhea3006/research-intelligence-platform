from api.database import insert_paper_chunks, get_connection
from ingestion.pdf_extractor import extract_pdf_text
from ingestion.section_detector import detect_sections
from ingestion.chunker import chunk_sections


ARXIV_ID = "2607.08374v1"
PDF_PATH = f"data/pdfs/{ARXIV_ID}.pdf"


print("📄 Extracting PDF...")
text = extract_pdf_text(PDF_PATH)

print("📚 Detecting sections...")
sections = detect_sections(text)

print("✂️ Chunking...")
chunks = chunk_sections(sections)

print(f"Sections: {len(sections)}")
print(f"Chunks: {len(chunks)}")


print("💾 Saving chunks to PostgreSQL...")
insert_paper_chunks(
    arxiv_id=ARXIV_ID,
    chunks=chunks,
)

print("✅ Chunks inserted successfully.")


# Verify database contents
conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        chunk_index,
        section_chunk_index,
        section,
        LENGTH(text)
    FROM paper_chunks
    WHERE arxiv_id = %s
    ORDER BY chunk_index
    """,
    (ARXIV_ID,),
)

rows = cursor.fetchall()

cursor.close()
conn.close()


print("\n📊 Database verification:")
print(f"Stored chunks: {len(rows)}")

for row in rows[:10]:
    print(row)

if len(rows) == len(chunks):
    print("\n🎉 Verification successful!")
else:
    print(
        f"\n⚠️ Expected {len(chunks)} chunks "
        f"but found {len(rows)}."
    )