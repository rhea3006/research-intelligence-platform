import "./PaperCard.css";
import type { Paper } from "../types/paper";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useSavedPapers } from "../context/SavedPapersContext";

type PaperCardProps = {
  paper: Paper;
};

function PaperCard({ paper }: PaperCardProps) {
  const {
    savePaper,
    removePaper,
    isPaperSaved,
  } = useSavedPapers();

  const saved = isPaperSaved(paper.arxiv_id);
  const handleSave = () => {
    if (saved) {
      removePaper(paper.arxiv_id);
    } else {
      savePaper(paper);
    }
  };

  return (
    <div className="paper-card">
      <h3>{paper.title}</h3>
        <p>👤 <strong>Authors:</strong> {paper.authors}</p>
        <p>📅 <strong>Published:</strong> {paper.published_date}</p>
        <p>⭐ <strong>Relevance:</strong> {paper.relevance_score}</p>
        <div className="paper-actions">
          <button
            className="save-btn"
            onClick={handleSave}
          >
            {saved ? "❤️ Saved" : "🤍 Save"}
          </button>
          <Link
            to={`/paper/${paper.arxiv_id}`}
            className="view-btn"
          >
            View Details →
          </Link>
        </div>
    </div>
  );
}

export default PaperCard;