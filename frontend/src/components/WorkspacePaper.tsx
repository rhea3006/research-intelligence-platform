import "./WorkspacePaper.css";
import type { Paper } from "../types/paper";
import { useWorkspace } from "../context/WorkspaceContext";

type WorkspacePaperProps = {
    paper: Paper;
    isSelected: boolean;
    onToggle: () => void;
};

function WorkspacePaper({ paper,isSelected,onToggle }: WorkspacePaperProps) {

    const { removePaper } = useWorkspace();

    const formattedDate = paper.published_date
        ? new Date(paper.published_date).toLocaleDateString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
          })
        : "Unknown";

    return (
        <div className="workspace-paper">
            <input
                type="checkbox"
                checked={isSelected}
                onChange={onToggle}
            />
            <div className="workspace-paper-content">

                <h3 className="workspace-paper-title">
                    📄 {paper.title}
                </h3>

                <p className="workspace-paper-authors">
                    {paper.authors}
                </p>

                <div className="workspace-paper-meta">

                    <span>{formattedDate}</span>

                    <span>
                        {paper.categories
                            .split(",")
                            .slice(0, 2)
                            .join(" • ")}
                    </span>

                </div>

            </div>

            <button
                className="remove-workspace-btn"
                onClick={() => removePaper(paper.arxiv_id)}
            >
                ✕ Remove
            </button>

        </div>
    );
}

export default WorkspacePaper;