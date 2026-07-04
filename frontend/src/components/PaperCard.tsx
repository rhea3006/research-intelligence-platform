import "./PaperCard.css";
import type { Paper } from "../types/paper";
import { Link } from "react-router-dom";

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