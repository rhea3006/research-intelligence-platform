import PaperCard from "../components/PaperCard";
import { useSavedPapers } from "../context/SavedPapersContext";
import "./SavedPapersPage.css";

function SavedPapersPage() {
    const { savedPapers } = useSavedPapers();

    return (
        <main className="saved-page">

            <h1 className="saved-title">
                ❤️ Saved Papers
            </h1>

            {savedPapers.length === 0 ? (
                <div className="empty-state">
                    <h2>📚 No saved papers yet</h2>

                    <p>
                        Save papers while browsing to build your personal reading list.
                    </p>
                </div>
            ) : (
                <section className="results">
                    {savedPapers.map((paper) => (
                        <PaperCard
                            key={paper.arxiv_id}
                            paper={paper}
                        />
                    ))}
                </section>
            )}

        </main>
    );
}

export default SavedPapersPage;