interface PaginationProps {
  page: number;
  totalPages: number;
  onPrevious: () => void;
  onNext: () => void;
}

function Pagination({
  page,
  totalPages,
  onPrevious,
  onNext,
}: PaginationProps) {
  return (
    <div className="pagination">

      <button
        className="page-btn"
        onClick={onPrevious}
        disabled={page === 1}
      >
        ← Previous
      </button>

      <span className="page-info">
        Page <strong>{page}</strong> of <strong>{totalPages}</strong>
      </span>

      <button
        className="page-btn"
        onClick={onNext}
        disabled={page >= totalPages}
      >
        Next →
      </button>

    </div>
  );
}

export default Pagination;