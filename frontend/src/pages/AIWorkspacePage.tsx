import { useState } from "react";
import { useWorkspace } from "../context/WorkspaceContext";
import WorkspacePaper from "../components/WorkspacePaper";
import { Link } from "react-router-dom";
import "./AIWorkspacePage.css";

function AIWorkspacePage() {
    const {
        workspacePapers,
        clearWorkspace,
    } = useWorkspace();

    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");
    const uniqueAuthors = new Set(
        workspacePapers.flatMap((paper) =>
            paper.authors.split(",").map((author) => author.trim())
        )
    ).size;
    const uniqueCategories = new Set(
        workspacePapers.flatMap((paper) =>
            paper.categories.split(",").map((category) => category.trim())
        )
    ).size;
    const suggestedPrompts = [
    "Compare the methodologies used in these papers.",
    "Summarize the key contributions of each paper.",
    "Identify common research gaps across these papers.",
    "Explain these papers as if I'm a beginner.",
    "What future research directions do these papers suggest?",
    ];

    return (
        <main className="workspace-page">
            <section className="workspace-header">
                <h1>🧠 AI Workspace</h1>
                <p>
                    Select research papers and ask AI to analyze,
                    summarize, compare, or explain them.
                </p>
            </section>
            {workspacePapers.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">
                   🧠
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
                          <h3>{workspacePapers.length}</h3>
                          <p>📄 Papers</p>
                      </div>
                      <div className="stat-card">
                          <h3>{uniqueAuthors}</h3>
                          <p>👤 Authors</p>
                      </div>
                      <div className="stat-card">
                          <h3>{uniqueCategories}</h3>
                          <p>🏷 Categories</p>
                      </div>
                  </div>
                  <div className="workspace-title">
                    <h2>
                        Selected Papers ({workspacePapers.length})
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
                        />
                      ))}
                    </div>
                  </section>
                  <section className="prompt-section">
                    <h2>Ask AI</h2>
                      <p className="prompt-subtitle">
                          Not sure where to start? Try one of these:
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
                        <textarea
                          placeholder="Example: Compare the methodologies of these papers and explain which approach is likely to generalize better."
                          value={prompt}
                          onChange={(e) => setPrompt(e.target.value)}
                          onInput={(e) => {
                             e.currentTarget.style.height = "auto";
                             e.currentTarget.style.height =
                             `${e.currentTarget.scrollHeight}px`;
                          }}
                        />
                        <button
                          className="generate-btn"
                            disabled={
                              workspacePapers.length === 0 ||
                              prompt.trim() === ""
                            }
                          >
                              ✨ Generate AI Analysis
                        </button>
                    </section>
                    <section className="response-section">
                        <div className="response-header">
                            <h2>🤖 AI Response</h2>

                            {response && (
                                <button className="copy-response-btn">
                                    📋 Copy
                                </button>
                            )}

                        </div>

                        <div className="response-box">

                            {response ? (

                                <div className="ai-response">

                                    {response}

                                </div>

                            ) : (

                                <div className="response-placeholder">

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
