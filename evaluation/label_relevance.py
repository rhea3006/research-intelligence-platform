import json
from pathlib import Path


LABEL_FILE = Path("evaluation/relevance_labels.json")


def load_labels():
    with open(LABEL_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_labels(data):
    with open(LABEL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def label_relevance():
    data = load_labels()

    print("=" * 70)
    print("RETRIEVAL RELEVANCE LABELING")
    print("=" * 70)
    print()
    print("Labels:")
    print("  3 = Highly relevant")
    print("  2 = Relevant")
    print("  1 = Marginally relevant")
    print("  0 = Not relevant")
    print("  s = Skip")
    print("  q = Quit and save progress")
    print()

    for query, papers in data.items():

        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)

        for i, paper in enumerate(papers, start=1):

            # Skip already-labelled papers
            if paper["relevance"] is not None:
                continue

            print("\n" + "-" * 70)
            print(f"Paper {i}/{len(papers)}")
            print("-" * 70)

            print(f"\nTitle:\n{paper['title']}")

            if paper.get("abstract"):
                print(f"\nAbstract:\n{paper['abstract']}")

            while True:
                value = input(
                    "\nRelevance [0/1/2/3 | s=skip | q=quit]: "
                ).strip().lower()

                if value == "q":
                    save_labels(data)
                    print("\n💾 Progress saved.")
                    return

                if value == "s":
                    print("Skipped.")
                    break

                if value in {"0", "1", "2", "3"}:
                    paper["relevance"] = int(value)
                    save_labels(data)
                    break

                print("Invalid input. Enter 0, 1, 2, 3, s, or q.")

    save_labels(data)

    print("\n" + "=" * 70)
    print("✅ ALL LABELS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    label_relevance()