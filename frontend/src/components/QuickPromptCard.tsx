import type { ReactNode } from "react";
import "./QuickPromptCard.css"

interface QuickPromptCardProps {
    icon: ReactNode;
    title: string;
    description: string;
    selected: boolean;
    onClick: () => void;
}

export default function QuickPromptCard({
    icon,
    title,
    description,
    selected,
    onClick,
}: QuickPromptCardProps) {
    return (
        <button
            className={`quick-prompt-card ${
                selected ? "selected" : ""
            }`}
            onClick={onClick}
        >
            <div className="quick-prompt-icon">
                {icon}
            </div>

            <div className="quick-prompt-content">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
        </button>
    );
}