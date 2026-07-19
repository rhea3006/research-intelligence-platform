import { Search } from "lucide-react";
import "./SearchBar.css"

type SearchBarProps = {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  onSearch: () => void;
  onClear: () => void;
  loading: boolean;
};


function SearchBar({query,setQuery,onSearch,onClear,loading}: SearchBarProps){
  return (
  <section className="search-section">

    <div className="search-container">

      <div className="search-input-wrapper">

          <Search size={22} className="search-icon" />

          <input
              type="text"
              className="search-input"
              placeholder="Search research papers..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => {
                  if (event.key === "Enter" && !loading) {
                      onSearch();
                  }
              }}
          />

      </div>

      <button
          className="search-btn"
          onClick={onSearch}
          disabled={loading}
      >
          {loading ? "Searching..." : "Search"}
      </button>

      {query && (
        <button
          className="clear-btn"
          onClick={onClear}
          disabled={loading}
      >
          Clear
      </button>
      )}

    </div>

  </section>
);
}

export default SearchBar;