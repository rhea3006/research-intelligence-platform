import "./EmptyState.css";

type EmptyStateProps = {
    icon: React.ReactNode;
    title: string;
    description: string;
    showSuggestions?: boolean;
    hasFilters?: boolean;
    onClearFilters?: () => void;
};

function EmptyState({
    icon,
    title,
    description,
    showSuggestions = false,
    hasFilters = false,
    onClearFilters,
}: EmptyStateProps) {
    return (
        <div className="empty-state">
            <div className="empty-icon">
                {icon}
            </div>

            <h2>{title}</h2>

            <p>{description}</p>

            {showSuggestions && (
                <div className="empty-suggestions">
                    <h4>Suggestions</h4>

                    <ul>
                        <li>Check your spelling</li>
                        <li>Try broader keywords</li>
                        <li>Use fewer search filters</li>
                    </ul>
                </div>
            )}

            {hasFilters && onClearFilters && (
                <button
                    className="empty-action-btn"
                    onClick={onClearFilters}
                >
                    Clear Filters
                </button>
            )}
        </div>
    );
}

export default EmptyState;