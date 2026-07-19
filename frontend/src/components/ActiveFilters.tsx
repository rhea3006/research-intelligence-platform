import "./ActiveFilters.css"

interface ActiveFiltersProps {
  category: string;
  author: string;
  year: string;

  setCategory: (value: string) => void;
  setAuthor: (value: string) => void;
  setYear: (value: string) => void;
}

function ActiveFilters({
  category,
  author,
  year,
  setCategory,
  setAuthor,
  setYear,
}: ActiveFiltersProps) {

  const hasFilters = category || author || year;

  if (!hasFilters) return null;

  return (
    <div className="active-filters">

      <div className="filter-chips">

        {category && (
        <button
            className="filter-chip"
            onClick={() => setCategory("")}
        >
            📚 {category}
            <span>✕</span>
        </button>
        )}

        {author && (
          <button
            className="filter-chip"
            onClick={() => setAuthor("")}
          >
            👤 {author}
            <span>✕</span>
          </button>
        )}

        {year && (
          <button
            className="filter-chip"
            onClick={() => setYear("")}
          >
            📅 {year}
            <span>✕</span>
          </button>
        )}

      </div>

      <button
        className="clear-filters"
        onClick={() => {
            setCategory("");
            setAuthor("");
            setYear("");
        }}
        >
        Clear All
      </button>

    </div>
  );
}

export default ActiveFilters;