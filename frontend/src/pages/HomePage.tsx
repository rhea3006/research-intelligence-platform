import '../App.css'
import "./HomePage.css";
import { useEffect, useState } from "react";
import HeroSection from "../components/HeroSection";
import SearchBar from "../components/SearchBar";
import { searchPapers } from "../services/api";
import type { Paper } from "../types/paper";
import PaperCard from "../components/PaperCard";
import SearchFilters from "../components/SearchFilters";
import LoadingSpinner from "../components/LoadingSpinner";
import EmptyState from "../components/EmptyState";
import Pagination from "../components/Pagination";
import ActiveFilters from '../components/ActiveFilters';
import PaperCardSkeleton from "../components/PaperCardSkeleton";
import { Search, SearchX } from "lucide-react";

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

  useEffect(() => {console.log("papers state:", papers);}, [papers]);
    
  const handleSearch = async (pageNumber = page) => {
    setHasSearched(true);
    setLoading(true);
    setError("");

    try {
      const response = await searchPapers(query,category,author,year,sort,
        pageNumber);
      console.log(response.results);
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
      window.scrollTo({top: 0,behavior: "smooth",});
    }
  }, [page]);

  useEffect(() => {
    if (!hasSearched) return;

    setPage(1);
    handleSearch(1);
  }, [category, author, year, sort]);

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

  const handleClear = () => {setQuery("");setPapers([]);setError("");setHasSearched(false);};
  return (
    <>
      <main className="home-page">
        <div className="page-content">
          <HeroSection />
          <SearchBar
            query={query}
            loading={loading}
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
          <ActiveFilters
              category={category}
              author={author}
              year={year}
              setCategory={setCategory}
              setAuthor={setAuthor}
              setYear={setYear}
          />
          {error && (
            <div className="error-banner">
              ⚠️ {error}
            </div>
          )}
          {loading ? (
            <section className="results-section">
                <div className="results">
                    {Array.from({ length: 6 }).map((_, index) => (
                        <PaperCardSkeleton key={index} />
                    ))}
                </div>
            </section>
        ) : !hasSearched ? (
            <EmptyState
                icon={<Search size={60} strokeWidth={1.6} />}
                title="Search for research papers"
                description="Enter a keyword above to discover AI and Machine Learning research papers."
            />
        ) : papers.length === 0 ? (
            <EmptyState
                  icon={<SearchX size={60} strokeWidth={1.6} />}
                  title="No matching papers found"
                  description="We couldn't find any papers matching your search."
                  showSuggestions
                  hasFilters={Boolean(category || author || year)}
                  onClearFilters={() => {
                      setCategory("");
                      setAuthor("");
                      setYear("");
                  }}
              />
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
                </div>
                {papers.length > 0 && (
                    <Pagination
                      page={page}
                      totalPages={totalPages}
                      onPrevious={handlePrevious}
                      onNext={handleNext}
                      />
                  )}
            </section>
          )}
          </div>
      </main>
    </>
  );
}

export default HomePage;