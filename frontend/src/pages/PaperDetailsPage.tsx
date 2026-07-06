import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPaper } from "../services/api";
import type { PaperDetail } from "../types/paper";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import "./PaperDetailsPage.css";


function PaperDetailsPage() {

    // Read the ID from the URL
    const { arxiv_id } = useParams();
    console.log("Paper ID:", arxiv_id);

    // State
    const [paper, setPaper] = useState<PaperDetail | null>(null);
    const [relatedPapers, setRelatedPapers] = useState<Paper[]>([]);
    const [copied, setCopied] = useState(false);

    // 👇 ADD useEffect RIGHT HERE
    useEffect(() => {

        const fetchPaper = async () => {

            if (!arxiv_id) return;

            try {
                const result = await getPaper(arxiv_id);
                console.log("Paper returned:", result);
                setPaper(result.paper);
                setRelatedPapers(result.related_papers);
            } catch (error) {
                console.error(error);
            }

        };

        fetchPaper();

    }, [arxiv_id]);

    // Loading screen
    if (!paper) {
        return <p>Loading paper...</p>;
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
                        setCopied(true);
                        setTimeout(() => setCopied(false), 2000);
                    }}
                    >
                    📋 Copy Citation
                </button>
                <button
                    className="action-btn"
                    onClick={() =>
                        navigator.clipboard.writeText(
                        `${paper.authors}
                        "${paper.title}"
                        arXiv: ${paper.arxiv_id}
                        Published: ${paper.published_date}`
                        )
                    }
                >
                    🔗 Share
                </button>
            </div>
            {copied && (
                <p className="copy-message">
                    ✅ Citation copied!
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