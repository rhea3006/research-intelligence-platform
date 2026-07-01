import { useState } from 'react'
import './App.css'
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import SearchBar from "./components/SearchBar";
import { searchPapers } from "./services/api";

interface Paper {
  arxiv_id: string;
  title: string;
  authors: string;
  published_date: string;
  relevance_score: number;
} 

function App() {
  const [query, setQuery] = useState("");
  const [papers, setPapers] = useState<Paper[]>([]);
  const handleSearch = async () => {
    try {
      const results = await searchPapers(query);
      setPapers(results);
      console.log(results);

    } catch (error) {
      console.error(error);
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
        <div className="results">
          {papers.map((paper) => (
            <div className="paper-card" key={paper.arxiv_id}>
              <h3>{paper.title}</h3>
                  <p>
                      <strong>Authors:</strong> {paper.authors}
                  </p>
                  <p>
                      <strong>Published:</strong> {paper.published_date}
                  </p>
              <hr />
            </div>
          ))}
         </div>
      </main>
    </>
  );
}
export default App;
