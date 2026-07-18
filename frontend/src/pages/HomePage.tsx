import '../App.css'
import { useEffect, useState } from "react";
import HeroSection from "../components/HeroSection";
import SearchBar from "../components/SearchBar";
import { searchPapers } from "../services/api";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import SearchFilters from "../components/SearchFilters";
import LoadingSpinner from "../components/LoadingSpinner";
import Pagination from "../components/Pagination";

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
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [totalResults, setTotalResults] = useState(0);

    useEffect(() => {
  console.log("papers state:", papers);
}, [papers]);
    
      const handleSearch = async (pageNumber = page) => {
        setHasSearched(true);
        setLoading(true);
        setError("");

        try {
          const response = await searchPapers(
            query,
            category,
            author,
            year,
            sort,
            pageNumber
          );
          setPapers(response.results);
          setTotalPages(response.total_pages);
          setTotalResults(response.total);
        } catch (err) {
          console.error(err);
          setError("Couldn't connect to the server. Please try again.");
        } finally {
          setLoading(false);
        }
      };
      useEffect(() => {
        if (query.trim() !== "") {
          handleSearch();
        window.scrollTo({
          top: 0,
          behavior: "smooth",
      });
        }
      }, [page]);

      const handlePrevious = () => {
        if (page > 1) {
          setPage(page - 1);
        }
      };

      const handleNext = () => {
        if (page < totalPages) {
          setPage(page + 1);
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
          onSearch={() => {
            setPage(1);
            handleSearch(1);
          }}
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
            <section className="results-section">
              <h2 className="results-heading">
                Showing {(page - 1) * 10 + 1}
                  {"–"}
                  {Math.min(page * 10, totalResults)}
                  {" of "}
                  {totalResults}
                  {" papers"}
              </h2>
              <div className="results">
                {papers.map((paper) => (
                  <PaperCard
                    key={paper.arxiv_id}
                      paper={paper}
                  />
                ))}
                {papers.length > 0 && (
                  <Pagination
                    page={page}
                    totalPages={totalPages}
                    onPrevious={handlePrevious}
                    onNext={handleNext}
                    />
                )}
              </div>
          </section>
        )}
      </main>
    </>
  );
}

export default HomePage;