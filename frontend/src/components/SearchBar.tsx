import { Search } from "lucide-react";
import "./SearchBar.css"

type SearchBarProps = {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  onSearch: () => void;
  onClear: () => void;
};


function SearchBar({query,setQuery,onSearch,onClear}: SearchBarProps){
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
                  if (event.key === "Enter") {
                      onSearch();
                  }
              }}
          />

      </div>

      <button
          className="search-btn"
          onClick={onSearch}
      >
          Search
      </button>

      {query && (
          <button
              className="clear-btn"
              onClick={onClear}
          >
              Clear
          </button>
      )}

    </div>

  </section>
);
}

export default SearchBar;