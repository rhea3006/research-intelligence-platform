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

      <input
        type="text"
        className="search-input"
        placeholder="🔍 Search research papers..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            onSearch();
          }
        }}
      />

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