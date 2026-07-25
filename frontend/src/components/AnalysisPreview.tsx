import type { Analysis } from "../services/api";
import "./AnalysisPreview.css"
import MarkdownRenderer from "../components/MarkdownRenderer/MarkdownRenderer";
import { FileText, CheckCircle2, Calendar, Tag,Copy,Download,Trash2, } from "lucide-react";
import { getAnalysisLabel } from "../utils/analysisType";

type AnalysisPreviewProps = {
    analysis: Analysis | null;
};

function AnalysisPreview({ analysis }: AnalysisPreviewProps) {
    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(
                analysis?.generated_markdown ?? ""
            );
        } catch (err) {
            console.error(err);
        }
    };
    if (!analysis) {
        return (
            <div className="empty-preview">
                <div className="empty-preview-icon">
                    <FileText size={72} strokeWidth={1.5} />
                </div>

                <h2>No Analysis Selected</h2>

                <p>
                    Select a saved analysis from the sidebar to preview
                    its AI-generated report.
                </p>

                <div className="empty-preview-features">
                    <div className="empty-feature">
                        <CheckCircle2 size={18} />
                        <span> Read structured AI analyses </span>
                    </div>
                    <div className="empty-feature">
                        <CheckCircle2 size={18} />
                        <span> Review previous research </span>
                    </div>
                    <div className="empty-feature">
                        <CheckCircle2 size={18} />
                        <span> Manage your saved analyses </span>
                    </div>
                </div>
                <span className="empty-preview-tip">
                    ← Choose an analysis from the left
                </span>
            </div>
        );
    }

    return (
        <div className="analysis-preview">
            <div className="analysis-header">

                <div className="analysis-title-row">
                    <FileText className="analysis-title-icon" size={28} />

                    <h1>{analysis.title}</h1>
                </div>

                <div className="analysis-meta">

                    <div className="analysis-badge">
                        <Tag size={14} />
                        <span>
                            {getAnalysisLabel(analysis.analysis_type)}
                        </span>
                    </div>

                    <div className="analysis-created">
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
                <div className="analysis-actions">
                    <button
                        className="analysis-action-btn"
                        onClick={handleCopy}
                    >
                        <Copy size={16} />
                        <span>Copy</span>
                    </button>

                    <button className="analysis-action-btn">
                        <Download size={16} />
                        <span>Export</span>
                    </button>

                    <button
                        className="analysis-action-btn danger"
                    >
                        <Trash2 size={16} />
                        <span>Delete</span>
                    </button>
                </div>
                <div className="analysis-divider" />
            </div>

            <MarkdownRenderer
                content={analysis.generated_markdown}
            />

        </div>
    );
}

export default AnalysisPreview;