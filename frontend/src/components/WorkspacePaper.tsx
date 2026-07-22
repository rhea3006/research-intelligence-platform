import "./WorkspacePaper.css";
import type { Paper } from "../types/paper";
import {
    FileText,
    Trash2,
    Calendar,
    Users,
    Tag,
    Check,
} from "lucide-react";
import { useWorkspace } from "../context/WorkspaceContext";

type WorkspacePaperProps = {
    paper: Paper;
    isSelected: boolean;
    onToggle: () => void;
};

function WorkspacePaper({
    paper,
    isSelected,
    onToggle,
}: WorkspacePaperProps) {
    const { removePaper } = useWorkspace();

    const formattedDate = paper.published_date
        ? new Date(paper.published_date).toLocaleDateString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
          })
        : "Unknown";

    const authorCount = paper.authors
        ? paper.authors.split(",").length
        : 0;

    return (
        <div className={`paper ${isSelected ? "selected" : ""}`} onClick={onToggle}>
            <div
                className={`selection-indicator ${
                    isSelected ? "selected" : ""
                }`}
                onClick={(e) => {
                    e.stopPropagation();
                    onToggle();
                }}
            >
                {isSelected && (
                    <Check
                        size={14}
                        strokeWidth={3}
                    />
                )}
            </div>
            <div className="workspace-paper-header">
                <div className="paper-icon">
                    <FileText size={24} />
                </div>

                <div className="workspace-paper-content">
                    <h3 className="workspace-paper-title">
                        {paper.title}
                    </h3>

                    <p className="workspace-paper-authors">
                        {paper.authors}
                    </p>

                    <div className="workspace-paper-meta">
                        <span className="meta-chip">
                            <Calendar size={14} />
                            {formattedDate}
                        </span>

                        <span className="meta-chip">
                            <Tag size={14} />
                            {paper.categories
                                .split(",")
                                .slice(0, 2)
                                .join(" • ")}
                        </span>

                        <span className="meta-chip">
                            <Users size={14} />
                            {authorCount}{" "}
                            {authorCount === 1
                                ? "Author"
                                : "Authors"}
                        </span>
                    </div>
                </div>
            </div>
            <button
                className="remove-workspace-btn"
                onClick={(e) => {
                    e.stopPropagation();
                    removePaper(paper.arxiv_id);
                }}
            >
                <Trash2 size={18} />
            </button>
        </div>
    );
}

export default WorkspacePaper;