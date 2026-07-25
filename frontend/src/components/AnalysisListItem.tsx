import { FileText, Calendar } from "lucide-react";
import type { AnalysisSummary } from "../services/api";

type AnalysisListItemProps = {
    analysis: AnalysisSummary;
    isSelected: boolean;
    onClick: () => void;
};

function AnalysisListItem({ analysis, isSelected ,onClick }: AnalysisListItemProps) {
    return (
        <div
            className={`analysis-list-item ${isSelected ? "selected" : ""}`}
            onClick={onClick}
        >
            <div className="analysis-card-header">
                <FileText size={18} className="analysis-card-icon" />

                <h3>{analysis.title}</h3>
            </div>

            <span className="analysis-type">
                {analysis.analysis_type.replace("_", " ")}
            </span>

            <div className="analysis-date">
                <Calendar size={14} />

                <span>
                    {new Date(analysis.created_at).toLocaleDateString(
                        "en-GB",
                        {
                            day: "numeric",
                            month: "short",
                            year: "numeric",
                        }
                    )}
                </span>
            </div>

        </div>
    );
}

export default AnalysisListItem;