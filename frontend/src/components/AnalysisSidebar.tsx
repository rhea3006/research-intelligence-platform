import type { AnalysisSummary } from "../services/api";
import AnalysisListItem from "./AnalysisListItem";
import "./AnalysisSidebar.css"
import { Search } from "lucide-react";
import { useState } from "react";

type AnalysisSidebarProps = {
    analyses: AnalysisSummary[];
    selectedAnalysisId: number | null;
    onSelect: (id: number) => void;
};

function AnalysisSidebar({ analyses,selectedAnalysisId,onSelect }: AnalysisSidebarProps) {
    const [searchQuery, setSearchQuery] = useState("");
    const [sortBy] = useState("newest");

    const filteredAnalyses = analyses.filter((analysis) => {
        const query = searchQuery.toLowerCase();

        return (
            analysis.title.toLowerCase().includes(query) ||
            analysis.analysis_type.toLowerCase().includes(query)
        );
    });

    const sortedAnalyses = [...filteredAnalyses].sort((a, b) => {
        switch (sortBy) {
            case "oldest":
                return (
                    new Date(a.created_at).getTime() -
                    new Date(b.created_at).getTime()
                );

            case "title":
                return a.title.localeCompare(b.title);

            case "newest":
            default:
                return (
                    new Date(b.created_at).getTime() -
                    new Date(a.created_at).getTime()
                );
        }
    });

    return (
        <aside className="analysis-sidebar">

            <div className="sidebar-header">
                <p className="analysis-count">
                    {filteredAnalyses.length} saved analyses
                </p>

                <div className="analysis-search">
                    <Search size={18} className="search-icon" />

                    <input
                        type="text"
                        placeholder="Search analyses..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
                {/* Remove this for now */}
                {/* Sort dropdown */}

            </div>

            <div className="sidebar-divider" />

            <div className="analysis-list">
                {filteredAnalyses.length > 0 ? (
                    sortedAnalyses.map((analysis) => (
                        <AnalysisListItem
                            key={analysis.id}
                            analysis={analysis}
                            isSelected={selectedAnalysisId === analysis.id}
                            onClick={() => onSelect(analysis.id)}
                        />
                    ))
                ) : (
                    <div className="no-search-results">
                        <Search size={28} />
                        <p>No analyses found.</p>
                    </div>
                )}
            </div>

        </aside>
    );
}

export default AnalysisSidebar;