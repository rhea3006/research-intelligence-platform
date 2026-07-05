import PaperCard from "../components/PaperCard";
import { useSavedPapers } from "../context/SavedPapersContext";

function SavedPapersPage() {
  const { savedPapers } = useSavedPapers();

  return (
    <div className="saved-page">
      <h1>❤️ Saved Papers</h1>

      {savedPapers.length === 0 ? (
        <p>You haven't saved any papers yet.</p>
      ) : (
        savedPapers.map((paper) => (
          <PaperCard
            key={paper.arxiv_id}
            paper={paper}
          />
        ))
      )}
    </div>
  );
}

export default SavedPapersPage;