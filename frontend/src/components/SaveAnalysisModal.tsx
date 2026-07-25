import { useState, useEffect} from "react";
import "./SaveAnalysisModal.css"



type SaveAnalysisModalProps = {
    isOpen: boolean;
    onClose: () => void;
    onSave: (title: string) => void;
};


function SaveAnalysisModal({ isOpen, onClose, onSave }: SaveAnalysisModalProps) {
    const [title, setTitle] = useState("");

    useEffect(() => {
        if (!isOpen) {
            setTitle("");
        }
    }, [isOpen]);

    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === "Escape") {
                onClose();
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    return (
    <div className="save-modal-overlay"
        onClick={onClose}
    >
        <div className="save-modal"
            onClick={(e) => e.stopPropagation()}
        >
            <form
                className="save-modal-form"
                onSubmit={(e) => {
                    e.preventDefault();
                    onSave(title.trim());
                }}
            >
                <h2>Save Analysis</h2>

                <p className="save-modal-description">
                    Give your analysis a descriptive title so you can easily find it later.
                </p>

                <div className="save-modal-field">
                    <label htmlFor="analysis-title">
                        Title
                    </label>

                    <input
                        id="analysis-title"
                        type="text"
                        placeholder="Enter a title..."
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        autoFocus
                    />
                </div>

                <div className="save-modal-actions">
                    <button
                        type="button"
                        className="modal-btn modal-btn-secondary"
                        onClick={onClose}
                    >
                        Cancel
                    </button>

                    <button
                        type="submit"
                        className="modal-btn modal-btn-primary"
                        disabled={!title.trim()}
                    >
                        Save Analysis
                    </button>
                </div>
            </form>
        </div>
    </div>
);
}

export default SaveAnalysisModal;