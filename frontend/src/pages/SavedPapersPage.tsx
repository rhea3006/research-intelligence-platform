import { useEffect, useState } from "react";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import { getSavedPapers } from "../utils/savedPapers";

function SavedPapersPage() {
  const [savedPapers, setSavedPapers] = useState<Paper[]>([]);

  useEffect(() => {
    setSavedPapers(getSavedPapers());
  }, []);

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