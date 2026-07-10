import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPaper } from "../services/api";
import type { PaperDetail } from "../types/paper";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import LoadingSpinner from "../components/LoadingSpinner";
import "./PaperDetailsPage.css";


function PaperDetailsPage() {

    // Read the ID from the URL
    const { arxiv_id } = useParams();

    // State
    const [paper, setPaper] = useState<PaperDetail | null>(null);
    const [relatedPapers, setRelatedPapers] = useState<Paper[]>([]);
    const [linkCopied, setLinkCopied] = useState(false);
    const [copyMessage, setCopyMessage] = useState("");
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

            <div className="paper-meta">

                <p>
                👤 <strong>Authors:</strong> {paper.authors}
                </p>

                <p>
                📅 <strong>Published:</strong> {paper.published_date}
                </p>

                <p>
                🏷️ <strong>Categories:</strong> {paper.categories}
                </p>

            </div>
            <div className="paper-actions">
                <a
                    href={paper.arxiv_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="action-btn"
                >
                    🌐 View on arXiv
                </a>
                <a
                    href={`https://research-intelligence-platform.onrender.com/papers/${paper.arxiv_id}/download`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="action-btn"
                >
                    📑 Download PDF
                </a>
                <button
                    className="action-btn"
                    onClick={() => {
                        navigator.clipboard.writeText(
                        `${paper.authors}
                        "${paper.title}"
                        arXiv: ${paper.arxiv_id}
                        Published: ${paper.published_date}`
                        );
                        setCopyMessage("✅ Citation copied!");
                        setTimeout(() => setCopyMessage(""), 2000);
                    }}
                    >
                    📋 Copy Citation
                </button>
                <button
                    className="action-btn"
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
                    🔗 Share
                </button>
            </div>
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
            <section className="abstract-section">

                <h2>Abstract</h2>

                <p>{paper.abstract}</p>
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