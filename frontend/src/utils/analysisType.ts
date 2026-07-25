export const ANALYSIS_LABELS: Record<string, string> = {
    compare: "Compare Papers",
    literature_review: "Literature Review",
    methodology_analysis: "Methodology Analysis",
    critical_evaluation: "Critical Evaluation",
    practical_applications: "Practical Applications",
};

export function getAnalysisLabel(type: string): string {
    return ANALYSIS_LABELS[type] ?? type;
}