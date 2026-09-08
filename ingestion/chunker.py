import re


CHUNK_SIZE = 4000
OVERLAP = 500


def normalize_paragraphs(text: str) -> list[str]:
    """
    Reconstruct paragraphs from PDF-extracted text.

    PDF extraction often inserts line breaks in the middle
    of sentences. This function converts those artificial
    line breaks into spaces while preserving paragraph boundaries.
    """

    # Normalize whitespace within lines
    lines = [
        re.sub(r"\s+", " ", line).strip()
        for line in text.splitlines()
    ]

    paragraphs = []
    current = []

    for line in lines:

        if not line:
            if current:
                paragraph = " ".join(current)

                # Repair words split across PDF line breaks.
                paragraph = re.sub(r"(\w)-\s+(\w)", r"\1\2", paragraph)

                paragraphs.append(paragraph)
                current = []

            continue

        current.append(line)

    if current:
        paragraph = " ".join(current)
        paragraph = re.sub(r"(\w)-\s+(\w)", r"\1\2", paragraph)
        paragraphs.append(paragraph)

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[str]:
    """
    Split text into overlapping chunks while respecting paragraphs.
    """

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    paragraphs = normalize_paragraphs(text)

    chunks = []
    current = ""

    for paragraph in paragraphs:

        # ---------------------------------------------------------
        # Normal case: paragraph fits in current chunk
        # ---------------------------------------------------------

        candidate = (
            f"{current}\n\n{paragraph}"
            if current
            else paragraph
        )

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        # ---------------------------------------------------------
        # Current chunk is full
        # ---------------------------------------------------------

        if current:
            chunks.append(current.strip())

        # ---------------------------------------------------------
        # Paragraph itself is too large
        # ---------------------------------------------------------

        if len(paragraph) > chunk_size:

            start = 0

            while start < len(paragraph):

                end = start + chunk_size

                chunk = paragraph[start:end].strip()

                if chunk:
                    chunks.append(chunk)

                start = end - overlap

            current = ""

        else:
            current = paragraph

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_sections(
    sections: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[dict]:
    """
    Chunk each section independently.

    Returns chunks with both:
        - global chunk_index
        - section-local chunk_index
    """

    chunks = []

    global_index = 0

    for section in sections:

        section_name = section["section"]

        section_chunks = chunk_text(
            section["text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for section_index, text in enumerate(section_chunks):

            chunks.append(
                {
                    "chunk_index": global_index,
                    "section_chunk_index": section_index,
                    "section": section_name,
                    "text": text,
                }
            )

            global_index += 1

    return chunks