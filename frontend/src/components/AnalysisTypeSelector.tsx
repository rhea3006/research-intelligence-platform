import {Microscope,BookOpen,ShieldCheck, Rocket} from "lucide-react";
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
        id: "methodology",
        icon: <Microscope size={26} />,
        title: "Methodology Analysis",
        description:
            "Discuss datasets, models, evaluation metrics, experimental design, strengths and weaknesses of each approach.",
    },
    {
        id: "literature_review",
        icon: <BookOpen size={26} />,
        title: "Literature Review",
        description:
            "Generate a structured review across selected papers.",
    },
    {
        id: "critical_evaluation",
        icon: <ShieldCheck size={26} />,
        title: "Critical Evaluation",
        description:
            "Identify assumptions, limitations, potential biases, threats to validity and opportunities for improvement.",
    },
    {
        id: "applications",
        icon: <Rocket size={26} />,
        title: "Real-World Applications",
        description:
            "Describe where these techniques can be used in industry, real-world systems and future products.",
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
                <h3>Choose Analysis Perspective</h3>
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