import { useState } from "react";

type SearchBarProps = {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  onSearch: () => void;
  onClear: () => void;
};


function SearchBar({query,setQuery,onSearch,onClear}: SearchBarProps){
  return (
    <section>
      <input
        type="text"
        placeholder="Search research papers..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            onSearch();
          }
        }}
      />
      <button onClick={onSearch}>
        Search
      </button>
      {query && (
        <button onClick={onClear}>
          Clear
        </button>
      )}
    </section>
  );
}

export default SearchBar;