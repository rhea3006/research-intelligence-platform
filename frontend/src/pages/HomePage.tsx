import { useState } from 'react'
import '../App.css'
import HeroSection from "../components/HeroSection";
import SearchBar from "../components/SearchBar";
import { searchPapers } from "../services/api";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import SearchFilters from "../components/SearchFilters";
import LoadingSpinner from "../components/LoadingSpinner";


function HomePage() {
    const [query, setQuery] = useState("");
      const [papers, setPapers] = useState<Paper[]>([]);
      const [loading, setLoading] = useState(false);
      const [hasSearched, setHasSearched] = useState(false);
      const [error, setError] = useState("");
      const [category, setCategory] = useState("");
      const [author, setAuthor] = useState("");
      const [year, setYear] = useState("");
      const [sort, setSort] = useState("relevance");
    
      const handleSearch = async () => {
        setHasSearched(true);
        setLoading(true);
        setError("");
    
        try {
          const results = await searchPapers(query,category,author,year,sort);
          setPapers(results);
        } 
        catch (err) {
          console.error(err);
          setError("Couldn't connect to the server. Please try again.");
        }
        finally {
          setLoading(false);
        }
      };
      const handleClear = () => {
        setQuery("");
        setPapers([]);
        setError("");
        setHasSearched(false);
      };
  return (
    <>
      <main>
        <HeroSection />
        <SearchBar 
          query={query} 
          setQuery={setQuery} 
          onSearch={handleSearch} 
          onClear={handleClear}
        />
        <SearchFilters
          category={category}
          setCategory={setCategory}
          author={author}
          setAuthor={setAuthor}
          year={year}
          setYear={setYear}
          sort={sort}
          setSort={setSort}
        />
        {error && (
          <div className="error-banner">
            ⚠️ {error}
           </div>
        )}
        {loading ? (
          <LoadingSpinner />
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

export default HomePage;