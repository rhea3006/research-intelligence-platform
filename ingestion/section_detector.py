import re


TOP_LEVEL_PATTERN = re.compile(
    r"^(?P<number>"
    r"I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII|XIV|XV"
    r")\.\s+"
    r"(?P<title>[A-Z][A-Z0-9 \-:&',()]+)$"
)


NUMBERED_PATTERN = re.compile(
    r"^(?P<number>\d+(?:\.\d+)*)\.?\s+"
    r"(?P<title>[A-Z][A-Za-z0-9 \-:&',()]+)$"
)

TERMINAL_SECTION_PATTERN = re.compile(
    r"^(ABSTRACT|REFERENCES|ACKNOWLEDGMENTS|ACKNOWLEDGEMENTS)$",
    re.IGNORECASE,
)


def normalize_title(title: str) -> str:
    """Normalize whitespace in a section title."""

    return re.sub(r"\s+", " ", title).strip()


def detect_sections(text: str) -> list[dict]:
    """
    Detect major academic paper sections.

    Supports formats such as:

        I. INTRODUCTION
        II. METHOD
        III. RESULTS

    and:

        1 Introduction
        2 Methodology
        3 Results

    Subsections such as:

        A. Baseline Acquisition

    remain inside their parent section.
    """

    lines = text.splitlines()

    sections = []

    current_section = "Front Matter"
    current_lines = []

    for line in lines:

        cleaned = line.strip()

        if not cleaned:
            current_lines.append("")
            continue
            # ---------------------------------------------------------
        # Terminal / unnumbered academic sections
        #
        # Examples:
        # ABSTRACT
        # REFERENCES
        # ACKNOWLEDGMENTS
        # ---------------------------------------------------------

        terminal_match = TERMINAL_SECTION_PATTERN.match(cleaned)

        if terminal_match:

            if current_lines:
                sections.append(
                    {
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                    }
                )

            current_section = terminal_match.group(1).upper()
            current_lines = []

            continue

        # ---------------------------------------------------------
        # IEEE-style Roman numeral heading
        #
        # Example:
        # I. INTRODUCTION
        # II. PROPOSED METHOD
        # III. EXPERIMENTS
        # ---------------------------------------------------------

        roman_match = TOP_LEVEL_PATTERN.match(cleaned)

        if roman_match:

            if current_lines:
                sections.append(
                    {
                        "section": current_section,
                        "text": "\n".join(current_lines).strip(),
                    }
                )

            number = roman_match.group("number")
            title = normalize_title(
                roman_match.group("title")
            )

            current_section = f"{number}. {title}"
            current_lines = []

            continue

        # ---------------------------------------------------------
        # Numbered academic heading
        #
        # Example:
        # 1 Introduction
        # 2 Methodology
        # ---------------------------------------------------------

        numbered_match = NUMBERED_PATTERN.match(cleaned)

        if numbered_match:

            number = numbered_match.group("number")
            title = normalize_title(
                numbered_match.group("title")
            )

            # Avoid interpreting ordinary numbered sentences
            # as section headings.
            if len(title.split()) <= 12:

                if current_lines:
                    sections.append(
                        {
                            "section": current_section,
                            "text": "\n".join(current_lines).strip(),
                        }
                    )

                current_section = f"{number} {title}"
                current_lines = []

                continue

        # ---------------------------------------------------------
        # Everything else belongs to the current section.
        # ---------------------------------------------------------

        current_lines.append(cleaned)

    # Add final section
    if current_lines:
        sections.append(
            {
                "section": current_section,
                "text": "\n".join(current_lines).strip(),
            }
        )

    return [
        section
        for section in sections
        if section["text"]
    ]