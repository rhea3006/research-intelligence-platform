import { useState } from 'react'
import './App.css'
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import SearchBar from "./components/SearchBar";
import { searchPapers } from "./services/api";
import type { Paper } from "./types/paper";
import PaperCard from "./components/PaperCard";

function App() {
  const [query, setQuery] = useState("");
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    setHasSearched(true);
    setLoading(true);
    try {
      const results = await searchPapers(query);
      setPapers(results);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <>
      <Navbar
        title="Research Intelligence Platform"
        subtitle="Search smarter. Discover faster."
      />
      <main>
        <HeroSection />
        <SearchBar query={query} setQuery={setQuery} onSearch={handleSearch}
        />
        {loading ? (
          <div className="empty-state">
              <h2>🔄 Searching papers...</h2>
              <p>Please wait while we fetch the latest research papers.</p>
          </div>
      ) : !hasSearched ? (
          <div className="empty-state">
              <h2>🔍 Search for research papers</h2>
              <p>
                  Enter a keyword above to discover AI and Machine Learning
                  research papers.
              </p>
          </div>
      ) : papers.length === 0 ? (
          <div className="empty-state">
              <h2>😔 No papers found</h2>
              <p>
                  Try another keyword or broaden your search.
              </p>
          </div>
      ) : (
          <>
              <h2 className="results-heading">
                  Showing {papers.length} papers
              </h2>
              <div className="results">
                  {papers.map((paper) => (
                      <PaperCard
                          key={paper.arxiv_id}
                          paper={paper}
                      />
                  ))}
              </div>
          </>
        )}
      </main>
    </>
  );
}
export default App;
