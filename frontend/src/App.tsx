import { useState } from 'react'
import './App.css'
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import SearchBar from "./components/SearchBar";
import { searchPapers } from "./services/api";

function App() {
  const [query, setQuery] = useState("");
  const handleSearch = async () => {
    try {
      const results = await searchPapers(query);

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
      </main>
    </>
  );
}
export default App;
