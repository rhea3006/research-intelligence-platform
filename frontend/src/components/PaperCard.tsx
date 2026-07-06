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
        <h3 className="paper-title">
            {paper.title}
        </h3>
        <p className="paper-authors">
            👤 {paper.authors}
        </p>
        <div className="paper-meta">
            <span>
                📅 {paper.published_date}
            </span>
            <span className="relevance-badge">
                ⭐ {paper.relevance_score}
            </span>
        </div>
        {/*<div className="category-list">
            {paper.categories.split(",").map((category) => (
                <span
                    key={category}
                    className="category-badge"
                >
                    {category.trim()}
                </span>
            ))}
        </div>*/}
        <Link
            to={`/paper/${paper.arxiv_id}`}
            className="view-btn"
        >
            View Details →
        </Link>
    </div>
  );
}

export default PaperCard;