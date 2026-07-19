import "./PaperCardSkeleton.css";

function PaperCardSkeleton() {
    return (
        <div className="paper-card skeleton-card">

            <div className="skeleton skeleton-title"></div>

            <div className="skeleton skeleton-authors"></div>

            <div className="skeleton skeleton-line"></div>
            <div className="skeleton skeleton-line"></div>
            <div className="skeleton skeleton-line short"></div>

            <div className="skeleton-chip-row">
                <div className="skeleton skeleton-chip"></div>
                <div className="skeleton skeleton-chip"></div>
            </div>

            <div className="skeleton skeleton-date"></div>

            <div className="skeleton skeleton-button"></div>

        </div>
    );
}

export default PaperCardSkeleton;