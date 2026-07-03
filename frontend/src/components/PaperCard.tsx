import "./PaperCard.css";
import type { Paper } from "../types/paper";

type PaperCardProps = {
  paper: Paper;
};

function PaperCard({ paper }: PaperCardProps) {
  return (
    <div className="paper-card">
      <h3>{paper.title}</h3>
        <p>👤 <strong>Authors:</strong> {paper.authors}</p>
        <p>📅 <strong>Published:</strong> {paper.published_date}</p>
        <p>⭐ <strong>Relevance:</strong> {paper.relevance_score}</p>
        <button className="view-btn">
            View Paper →
        </button>
    </div>
  );
}

export default PaperCard;