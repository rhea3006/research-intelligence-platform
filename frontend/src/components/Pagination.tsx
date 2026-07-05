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
        onClick={onPrevious}
        disabled={page === 1}
      >
        ← Previous
      </button>

      <span>
        Page {page} of {totalPages}
      </span>

      <button
        onClick={onNext}
        disabled={page >= totalPages}
      >
        Next →
      </button>
    </div>
  );
}

export default Pagination;