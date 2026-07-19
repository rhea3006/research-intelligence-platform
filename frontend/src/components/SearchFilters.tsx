import "./SearchFilters.css"
import {Tag,User,CalendarDays,ArrowUpDown,} from "lucide-react";


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
    <div className="filter-input-wrapper">
      <Tag size={16} className="filter-icon" />

      <input
          className="filter-input"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
      />
    </div>

    <div className="filter-input-wrapper">
        <User size={16} className="filter-icon" />

        <input
            className="filter-input"
            placeholder="Author"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
        />
    </div>
    <div className="filter-input-wrapper">
        <CalendarDays size={16} className="filter-icon" />

        <input
            className="filter-input"
            placeholder="Year"
            value={year}
            onChange={(e) => setYear(e.target.value)}
        />
    </div>
    <div className="filter-select-wrapper">
      <ArrowUpDown size={16} className="filter-icon" />

      <select
          className="filter-select"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
      >
          <option value="relevance">Relevance</option>
          <option value="newest">Newest</option>
          <option value="oldest">Oldest</option>
      </select>
    </div>
  </section>
);
}

export default SearchFilters;