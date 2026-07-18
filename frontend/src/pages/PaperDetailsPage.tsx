import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import type { PaperDetail } from "../types/paper";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { getPaper, summarizePaper } from "../services/api";
import ReactMarkdown from "react-markdown";
import "./PaperDetailsPage.css";
import {Users,CalendarDays,Tag,Globe,FileDown,Copy,Share2,FileText,Sparkles,} from "lucide-react";


function PaperDetailsPage() {

    // Read the ID from the URL
    const { arxiv_id } = useParams();

    //  Component States 
    const [activeTab, setActiveTab] = useState<"abstract" | "summary">("abstract");
    const [paper, setPaper] = useState<PaperDetail | null>(null);
    const [relatedPapers, setRelatedPapers] = useState<Paper[]>([]);
    const [linkCopied, setLinkCopied] = useState(false);
    const [copyMessage, setCopyMessage] = useState("");
    const [aiResponse, setAiResponse] = useState("");
    const [loadingAI, setLoadingAI] = useState(false);
    const [error, setError] = useState("");

    // 👇 ADD useEffect RIGHT HERE
    useEffect(() => {
        window.scrollTo({
        top: 0,
        behavior: "smooth",
        });

    const fetchPaper = async () => {
        if (!arxiv_id) return;
        setPaper(null);
        setRelatedPapers([]);
        setError("");

        try {
            const result = await getPaper(arxiv_id);
            setPaper(result.paper);
            setRelatedPapers(result.related_papers);
        } catch (error) {
            console.error(error);
            setError("Couldn't load this paper.");
        }
    };
    fetchPaper();

    }, [arxiv_id]);

    const handleSummarize = async () => {
    if (!paper) return;

    setLoadingAI(true);
    setAiResponse("");

    try {
        const result = await summarizePaper(paper.arxiv_id);

        setAiResponse(result.summary);
    } catch (error) {
        console.error(error);
        setAiResponse(
            "Sorry, something went wrong while generating the summary."
        );
    } finally {
        setLoadingAI(false);
    }
};

    
    if (error) {
        return (
            <main className="paper-page">
                <div className="empty-state">
                    <h2>📄 Paper not found</h2>
                    <p>{error}</p>
                </div>
            </main>
        );
    }
    if (!paper) {
    return <LoadingSpinner />;
    }

    const pdfUrl = paper.arxiv_url.replace("/abs/", "/pdf/") + ".pdf";
    const formatDate = (date: string) =>
    new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });

    // Main UI
    return (
        <main className="paper-page">

            <button
            className="back-button"
            onClick={() => window.history.back()}
            >
            ← Back to Search
            </button>

            <article className="paper-container">

            <h1 className="paper-title">
                {paper.title}
            </h1>
            <div className="paper-meta-grid">
                <div className="meta-card">
                    <Users size={18} />
                    <div>
                        <span className="meta-label">Authors</span>
                        <p>{paper.authors}</p>
                    </div>
                </div>

                <div className="meta-card">
                    <CalendarDays size={18} />
                    <div>
                        <span className="meta-label">Published</span>
                        <p>{formatDate(paper.published_date)}</p>
                    </div>
                </div>

                <div className="meta-card">
                    <Tag size={18} />
                    <div>
                        <span className="meta-label">Categories</span>
                        <p>{paper.categories}</p>
                    </div>
                </div>
            </div>
            <div className="action-btn secondary-btn">
                <a
                    href={paper.arxiv_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="action-btn secondary-btn"
                >
                    <Globe size={18} />
                        <span>View on arXiv</span>
                </a>
                <a
                    href={`https://research-intelligence-platform.onrender.com/papers/${paper.arxiv_id}/download`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="action-btn secondary-btn"
                >
                    <FileDown size={18} />
                        <span>Download PDF</span>   
                </a>
                <button
                    className="action-btn secondary-btn"
                    onClick={() => {
                        navigator.clipboard.writeText(
                        `${paper.authors}
                        "${paper.title}"
                        arXiv: ${paper.arxiv_id}
                        Published: ${paper.published_date}`
                        );
                        setCopyMessage("Citation copied!");
                        setTimeout(() => setCopyMessage(""), 2000);
                    }}
                    >
                    <Copy size={18} />
                        <span>Copy Citation</span>
                </button>
                <button
                    className="action-btn secondary-btn"
                    onClick={async () => {
                        const url = window.location.href;
                        try {
                            if (navigator.share) {
                                await navigator.share({
                                    title: paper.title,
                                    url,
                                });
                            } else {
                                await navigator.clipboard.writeText(url);
                                setLinkCopied(true);
                                setTimeout(() => setLinkCopied(false), 2000);
                            }
                        } catch (error) {
                            console.error(error);
                        }
                    }}
                >
                    <Share2 size={18} />
                        <span>Share</span>
                </button>
            </div>
            <hr className="section-divider" />

            {copyMessage && (
                <p className="copy-message">
                    {copyMessage}
                </p>
            )}
            {linkCopied && (
                <p className="copy-message">
                    🔗 Link copied!
                </p>
            )}
            <section className="paper-tabs-section">
                <div className="paper-tabs">
                    <button
                        className={activeTab === "abstract" ? "active-tab" : ""}
                        onClick={() => setActiveTab("abstract")}
                    >
                        <FileText size={18} />
                            <span>Abstract</span>
                    </button>

                    <button
                        className={activeTab === "summary" ? "active-tab" : ""}
                        onClick={() => setActiveTab("summary")}
                    >
                        <Sparkles size={18} />
                            <span>AI Summary</span>
                    </button>
                </div>
                {activeTab === "abstract" && (
                    <div className="tab-content">
                        <h2>Abstract</h2>
                        <p>{paper.abstract}</p>
                    </div>
                )}
                {activeTab === "summary" && (
                    <div className="tab-content">
                        <div className="ai-header">
                            <h2>🤖 AI Research Assistant</h2>
                            <p>
                                Generate an AI-powered understanding of this paper.
                            </p>
                            <button
                                className="action-btn ai-btn"
                                onClick={handleSummarize}
                                disabled={loadingAI}
                            >
                                {loadingAI
                                    ? "Generating Summary..."
                                    : "📝 Generate AI Summary"}
                            </button>
                        </div>
                        {aiResponse && (
                            <div className="ai-response">
                                <h3>✨ AI Summary</h3>
                                <div className="markdown-content">
                                    <ReactMarkdown>
                                        {aiResponse}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        )}
                    </div>
                )}

            </section>
            <section className="related-section">
                <h2>Related Papers</h2>
                <div className="related-grid">
                    {relatedPapers.map((paper) => (
                        <PaperCard
                            key={paper.arxiv_id}
                            paper={paper}
                        />
                    ))}
                </div>
            </section>
            </article>
        </main>
    );
}

export default PaperDetailsPage;