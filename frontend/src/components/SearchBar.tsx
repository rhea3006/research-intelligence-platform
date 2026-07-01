import { useState } from "react";

type SearchBarProps = {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;
  onSearch: () => void;
};


function SearchBar({query,setQuery,onSearch,}: SearchBarProps){
  const handleSearch = () => {
    console.log("Searching for:", query);
  };

  return (
    <section>
      <input
        type="text"
       placeholder="Search research papers..."
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />

      <button onClick={onSearch}>
        Search
      </button>
    </section>
  );
}

export default SearchBar;