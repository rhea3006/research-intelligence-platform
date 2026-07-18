import "./SearchFilters.css"

type SearchFiltersProps = {
  category: string;
  setCategory: React.Dispatch<React.SetStateAction<string>>;

  author: string;
  setAuthor: React.Dispatch<React.SetStateAction<string>>;

  year: string;
  setYear: React.Dispatch<React.SetStateAction<string>>;

  sort: string;
  setSort: React.Dispatch<React.SetStateAction<string>>;
};

function SearchFilters({
  category,
  setCategory,
  author,
  setAuthor,
  year,
  setYear,
  sort,
  setSort,
}: SearchFiltersProps) {
  return (
  <section className="filters">

    <input
      className="filter-input"
      placeholder="📂 Category"
      value={category}
      onChange={(e) => setCategory(e.target.value)}
    />

    <input
      className="filter-input"
      placeholder="👤 Author"
      value={author}
      onChange={(e) => setAuthor(e.target.value)}
    />

    <input
      className="filter-input"
      placeholder="📅 Year"
      value={year}
      onChange={(e) => setYear(e.target.value)}
    />

    <select
      className="filter-select"
      value={sort}
      onChange={(e) => setSort(e.target.value)}
    >
      <option value="relevance">
        ⭐ Relevance
      </option>

      <option value="newest">
        🆕 Newest
      </option>

      <option value="oldest">
        🕰️ Oldest
      </option>
    </select>

  </section>
);
}

export default SearchFilters;