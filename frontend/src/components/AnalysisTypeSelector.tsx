import {Scale,BookOpen,Search,GraduationCap,} from "lucide-react";
import type { AnalysisType } from "../services/api";
import type { ReactNode } from "react";


interface AnalysisTypeCard {
    id: AnalysisType;
    icon: ReactNode;
    title: string;
    description: string;
}

const analysisTypes: AnalysisTypeCard[] = [
    {
        id: "compare",
        icon: <Scale size={26} />,
        title: "Compare Papers",
        description:
            "Compare methodologies, strengths, weaknesses and findings.",
    },
    {
        id: "literature_review",
        icon: <BookOpen size={26} />,
        title: "Literature Review",
        description:
            "Generate a structured review across selected papers.",
    },
    {
        id: "research_gap",
        icon: <Search size={26} />,
        title: "Research Gap Analysis",
        description:
            "Identify limitations, unanswered questions and future work.",
    },
    {
        id: "beginner",
        icon: <GraduationCap size={26} />,
        title: "Beginner Explanation",
        description:
            "Explain the selected papers in simple language.",
    },
];

interface Props {
    selected: string;
    onSelect: (analysis: AnalysisType) => void;

}

function AnalysisTypeSelector({
    selected,
    onSelect,
}: Props) {
    return (
        <div className="analysis-selector">

            <div className="analysis-header">
                <h3>Choose Analysis Type</h3>
                <p>
                    Select how you want AI to analyze your research papers.
                </p>
            </div>

            <div className="analysis-grid">
                {analysisTypes.map((analysis) => (
                    <button
                        key={analysis.id}
                        type="button"
                        className={`analysis-card ${
                            selected === analysis.id ? "active" : ""
                        }`}
                        onClick={() => onSelect(analysis.id)}
                    >
                        <div className="analysis-icon">
                            {analysis.icon}
                        </div>

                        <h4>{analysis.title}</h4>

                        <p>{analysis.description}</p>
                    </button>
                ))}
            </div>

        </div>
    );
}

export default AnalysisTypeSelector;