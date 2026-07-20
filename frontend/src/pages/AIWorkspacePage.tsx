import { useState,useEffect} from "react";
import { useWorkspace } from "../context/WorkspaceContext";
import WorkspacePaper from "../components/WorkspacePaper";
import AnalysisTypeSelector from "../components/AnalysisTypeSelector";
import { analyzeWorkspace} from "../services/api";
import type { AnalysisType } from "../services/api";
import { Link } from "react-router-dom";
import { useRef } from "react";
import "./AIWorkspacePage.css";
import ReactMarkdown from "react-markdown";
import { BrainCircuit, FileText, Users, Tags, Sparkles, Bot, Copy,
    LoaderCircle} from "lucide-react";


function AIWorkspacePage() {
    const {
        workspacePapers,
        clearWorkspace,
    } = useWorkspace();

    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [showAdvanced, setShowAdvanced] = useState(false);
    const [analysisDepth, setAnalysisDepth] = useState("Standard");
    const [writingStyle, setWritingStyle] =useState("Academic");
    const [outputFormat, setOutputFormat] =useState("Structured Report");
    const [analysisType, setAnalysisType] =useState<AnalysisType>("compare");
    const [isGenerating, setIsGenerating] = useState(false);
    const responseRef = useRef<HTMLDivElement>(null);

    const uniqueAuthors = new Set(workspacePapers.flatMap((paper) =>
            paper.authors.split(",").map((author) => author.trim()))).size;

    const uniqueCategories = new Set(workspacePapers.flatMap((paper) =>
            paper.categories.split(",").map((category) => category.trim()))).size;

    const suggestedPrompts = [
        "Compare the methodologies used in these papers.",
        "Summarize the key contributions of each paper.",
        "Identify common research gaps across these papers.",
        "Explain these papers as if I'm a beginner.",
        "What future research directions do these papers suggest?",
    ];

    const togglePaperSelection = (paperId: string) => {
        setSelectedPaperIds((previous) =>
            previous.includes(paperId)
                ? previous.filter((id) => id !== paperId)
                : [...previous, paperId]
        );
    }
    const [selectedPaperIds, setSelectedPaperIds] = useState<string[]>([]);
    useEffect(() => {
        setSelectedPaperIds(
            workspacePapers.map((paper) => paper.arxiv_id)
        );
    }, [workspacePapers]);

    const selectedCount = selectedPaperIds.length;

    const getValidationMessage = () => {
        switch (analysisType) {
            case "compare":
                return selectedCount !== 2
                    ? "Select exactly two papers to compare."
                    : "";
            case "literature_review":
                return selectedCount < 2
                    ? "Select at least two papers."
                    : "";
            case "research_gap":
                return selectedCount < 3
                    ? "Select at least three papers."
                    : "";
            case "beginner":
                return selectedCount !== 1
                    ? "Select exactly one paper."
                    : "";
            default:
                return "";
        }

    };
    const validationMessage = getValidationMessage();
    const handleGenerate = async () => {
        setResponse("");
        setIsGenerating(true);

        try {
            setIsGenerating(true);

            const result = await analyzeWorkspace({
                paper_ids: selectedPaperIds,
                analysis_type: analysisType,
                additional_prompt: prompt,
                analysis_depth: analysisDepth,
                writing_style: writingStyle,
                output_format: outputFormat,
            });

            setResponse(result.analysis);
            setTimeout(() => {
                responseRef.current?.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });
            }, 100);

        } catch (error) {

            console.error(error);

            setResponse(
                "Failed to generate analysis. Please try again."
            );

        } finally {

            setIsGenerating(false);

        }
    };

    const handleCopy = async () => {
        await navigator.clipboard.writeText(response);
    };

    return (
        <main className="workspace-page">
            <section className="workspace-header">
                <h1 className="workspace-heading">
                    <BrainCircuit size={40} />
                    AI Workspace
                </h1>
                <p>
                    Select research papers and ask AI to analyze,
                    summarize, compare, or explain them.
                </p>
            </section>
            {workspacePapers.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">
                   <BrainCircuit size={72} strokeWidth={1.5} />
                </div>
                <h2>Your workspace is empty</h2>
                    <p>
                        Add research papers from Search Results
                        to begin AI-assisted analysis.
                    </p>
                    <Link
                        to="/"
                        className="browse-btn"
                    >
                        Browse Papers
                    </Link>
                </div>
            ) : (
                <>
                <section className="workspace-papers">
                    <div className="workspace-stats">
                        <div className="stat-card">
                            <FileText size={22} />
                            <h3>{workspacePapers.length}</h3>
                            <p>Papers</p>
                        </div>
                        <div className="stat-card">
                            <Users size={22} />
                            <h3>{uniqueAuthors}</h3>
                            <p>Authors</p>
                        </div>
                        <div className="stat-card">
                            <Tags size={22} />
                            <h3>{uniqueCategories}</h3>
                            <p>Categories</p>
                        </div>
                    </div>
                    <div className="workspace-title">
                        <h2>
                            Selected Papers ({selectedPaperIds.length} of {workspacePapers.length})
                        </h2>
                        <button
                            className="clear-workspace-btn"
                            onClick={clearWorkspace}
                        >
                            Clear Workspace
                        </button>
                    </div>
                    <div className="workspace-paper-list">
                        {workspacePapers.map((paper) => (
                            <WorkspacePaper
                                key={paper.arxiv_id}
                                paper={paper}
                                isSelected={selectedPaperIds.includes(paper.arxiv_id)}
                                onToggle={() => togglePaperSelection(paper.arxiv_id)}
                            />
                      ))}
                    </div>
                </section>
                <section className="prompt-section">
                    <h2>Configure Analysis</h2>
                    <p className="prompt-subtitle">
                        Choose an analysis type and optionally provide additional instructions.
                    </p>
                    <div className="prompt-suggestions">
                        {suggestedPrompts.map((suggestion) => (
                            <button
                              key={suggestion}
                              className="suggestion-btn"
                              onClick={() => setPrompt(suggestion)}
                            >
                              {suggestion}
                            </button>
                        ))}
                    </div>
                    <AnalysisTypeSelector
                        selected={analysisType}
                        onSelect={setAnalysisType}
                    />
                    <label className="textarea-label">
                        Additional Instructions <span>(Optional)</span>
                    </label>
                    <textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder={`Example:
                            • Focus on evaluation metrics

                            • Compare computational efficiency

                            • Ignore related work

                            • Highlight reproducibility`}
                        onInput={(e) => {
                            e.currentTarget.style.height = "auto";
                            e.currentTarget.style.height =
                            `${e.currentTarget.scrollHeight}px`;
                        }}
                    />
                    <button
                        className="advanced-toggle"
                        onClick={() => setShowAdvanced(!showAdvanced)}
                    >
                        {showAdvanced ? "▼" : "▶"} Advanced Settings
                    </button>
                    {showAdvanced && (
                        <div className="advanced-panel">
                            <div className="setting-group">
                                <label>Analysis Depth</label>
                                <div className="segment-control">
                                    {["Brief", "Standard", "Comprehensive"].map((depth) => (
                                        <button
                                            key={depth}
                                            type="button"
                                            className={`segment-btn ${
                                                analysisDepth === depth ? "active" : ""
                                            }`}
                                            onClick={() => setAnalysisDepth(depth)}
                                        >
                                            {depth}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="setting-group">
                                <label>Writing Style</label>
                                <div className="segment-control">
                                    {["Academic", "Beginner Friendly", "Technical"].map((style) => (
                                        <button
                                            key={style}
                                            type="button"
                                            className={`segment-btn ${
                                            writingStyle === style ? "active" : ""}`}
                                            onClick={() => setWritingStyle(style)}
                                        >
                                            {style}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="setting-group">
                                <label>Output Format</label>
                                <div className="segment-control">
                                    {[ "Structured Report",
                                        "Bullet Points",
                                        "Comparison Table",
                                    ].map((format) => (
                                        <button
                                            key={format}
                                            type="button"
                                            className={`segment-btn ${
                                            outputFormat === format ? "active" : ""}`}
                                            onClick={() => setOutputFormat(format)}
                                        >
                                            {format}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                    {validationMessage && (
                        <p className="validation-message">
                            {validationMessage}
                        </p>
                    )}
                    <button
                        className="generate-btn"
                        onClick={handleGenerate}
                        disabled={validationMessage !== "" || isGenerating}
                    >
                        {isGenerating ? (
                            <>
                                <LoaderCircle
                                    size={18}
                                    className="spinner"
                                />
                                Generating...
                            </>
                        ) : (
                            <>
                                <Sparkles size={18} />
                                Generate Analysis
                            </>
                        )}
                    </button>
                </section>
                <section 
                    ref={responseRef}
                    className="response-section"
                >
                    <div className="response-header">
                        <h2>
                            <Bot size={24} />
                            Generated Analysis
                        </h2>
                        {response && (
                            <button className="copy-response-btn"
                                onClick={handleCopy}
                            >
                                <Copy size={16} />
                                Copy
                            </button>
                        )}
                    </div>
                    <div className="response-box">
                        {response ? (
                            <div className="ai-response">
                                <ReactMarkdown>
                                    {response}
                                </ReactMarkdown>
                            </div>
                        ) : (
                            <div className="response-placeholder">
                                <BrainCircuit size={64}/>
                                <h3>No analysis generated yet</h3>
                                <p>
                                    Select papers, write a prompt,
                                    and click <strong>Generate AI Analysis</strong>.
                                </p>
                                <p>
                                    AI-generated summaries,
                                    comparisons and insights
                                    will appear here.
                                </p>
                            </div>
                        )}

                    </div>
                </section>
              </>
            )}
      </main>
    );
}

export default AIWorkspacePage;
