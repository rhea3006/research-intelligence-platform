import { useEffect, useState } from "react";
import { getAnalyses, type AnalysisSummary,getAnalysis,
type Analysis,} from "../services/api";
import AnalysisSidebar from "../components/AnalysisSidebar";
import AnalysisPreview from "../components/AnalysisPreview";
import { ArrowLeft, Files } from "lucide-react";
import "./MyAnalysesPage.css"



function MyAnalysesPage() {
    const [analyses, setAnalyses] = useState<AnalysisSummary[]>([]);
    const [, setLoading] = useState(true);
    const [selectedAnalysis, setSelectedAnalysis] =useState<Analysis | null>(null);

    
    const loadAnalyses = async () => {
        try {
            const data = await getAnalyses();
            setAnalyses(data);
        } catch (error) {
            console.error("Failed to load analyses:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadAnalyses();
    }, []);

    const handleSelectAnalysis = async (id: number) => {
        try {
            const analysis = await getAnalysis(id);
            setSelectedAnalysis(analysis);
        } catch (error) {
            console.error("Failed to load analysis:", error);
        }
    };

    return (
        <div className="page-container">
            <button
                    className="back-button"
                    onClick={() => window.history.back()}
                >
                    <ArrowLeft size={18} />
                    <span>Back</span>
                </button>
            <div className="page-header">
                <div className="page-title-icon">
                    <Files size={42} strokeWidth={1.8}/>
                </div>
                <h1>My Analyses</h1>
                <p>
                    Review, manage and export your saved AI-generated reports.
                </p>
            </div>
            <div className="analyses-layout">
                <AnalysisSidebar 
                    analyses={analyses}
                    selectedAnalysisId={selectedAnalysis?.id ?? null}
                    onSelect={handleSelectAnalysis}
                />
                <AnalysisPreview 
                    analysis={selectedAnalysis}
                />
            </div>
        </div>
    );
}

export default MyAnalysesPage;