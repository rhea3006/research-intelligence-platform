import "./PaperCard.css";
import type { Paper } from "../types/paper";
import { Link } from "react-router-dom";
import { useSavedPapers } from "../context/SavedPapersContext";
import { useWorkspace } from "../context/WorkspaceContext";
import {Users,CalendarDays,Heart,FolderPlus,FolderCheck,ArrowRight,} from "lucide-react";


type PaperCardProps = {
  paper: Paper;
};

function PaperCard({ paper }: PaperCardProps) {
  const {
    savePaper,
    removePaper,
    isPaperSaved,
  } = useSavedPapers();

  const {
        addPaper,
        removePaper: removeWorkspacePaper,
        isPaperSelected,
    } = useWorkspace();

  const inWorkspace = isPaperSelected(paper.arxiv_id);
  const isSaved = isPaperSaved(paper.arxiv_id);

  const handleSave = () => {
    if (isSaved) {
      removePaper(paper.arxiv_id);
    } else {
      savePaper(paper);
    }
  };
  const handleWorkspace = () => {
        if (inWorkspace) {
            removeWorkspacePaper(paper.arxiv_id);
        } else {
            addPaper(paper);
        }
    };

  const formattedDate = paper.published_date
    ? new Date(paper.published_date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        })
    : "Unknown";

  return (
    <div className="paper-card">
        <div className="paper-content">

            <Link
                to={`/paper/${paper.arxiv_id}`}
                className="paper-title-link"
            >
                <h3 className="paper-title">
                    {paper.title}
                </h3>
            </Link>
            <div className="paper-meta">
                <div className="paper-meta-item">
                    <Users size={15} />
                    <span>
                        {paper.authors
                            .split(",")
                            .slice(0, 3)
                            .join(", ")}
                        {paper.authors.split(",").length > 3 && " et al."}
                    </span>
                </div>

                <div className="paper-meta-item">
                    <CalendarDays size={15} />
                    <span>{formattedDate}</span>
                </div>
            </div>
            <div className="paper-footer">

                <div className="category-list">
                    {paper.categories
                        ?.split(",")
                        .slice(0,3)
                        .map(category => (
                            <span
                                key={category}
                                className="category-badge"
                            >
                                {category.trim()}
                            </span>
                    ))}
                </div>
            </div>
            <div className="paper-actions">
                <button
                    className={`save-btn ${isSaved ? "saved" : ""}`}
                    onClick={handleSave}
                >
                    <>
                        <Heart
                            size={18}
                            fill={isSaved ? "currentColor" : "none"}
                        />

                        {isSaved ? "Saved" : "Save"}
                    </>
                </button>
                <button
                    className={`workspace-btn ${
                        inWorkspace ? "selected" : ""
                    }`}
                    onClick={handleWorkspace}
                >
                    <>
                        {inWorkspace ? (
                            <FolderCheck size={18} />
                        ) : (
                            <FolderPlus size={18} />
                        )}

                        {inWorkspace
                            ? "Added"
                            : "Workspace"}
                    </>
                </button>
            </div>
        </div>
        <Link
            to={`/paper/${paper.arxiv_id}`}
            className="view-btn"
        >
            <>
                View Details

                <ArrowRight size={18}/>
            </>
        </Link>

    </div>
  );
}

export default PaperCard;