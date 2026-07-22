import ReactMarkdown from "react-markdown";
import type { ReactNode } from "react";
import "./MarkdownRenderer.css";
import {FileText,Target,Cpu,BarChart3,Lightbulb,AlertTriangle,Compass,Scale,
    GitCompare,Layers,Search,ArrowRight,GraduationCap,BookOpen,
    Bookmark} from "lucide-react";

interface MarkdownRendererProps {
    content: string;
}

const headingIcons: Record<string, ReactNode> = {
    // General
    "summary": <FileText size={20} />,
    "executive summary": <FileText size={20} />,
    "overview": <FileText size={20} />,

    // Comparison
    "comparison": <Scale size={20} />,
    "comparison summary": <Scale size={20} />,
    "key differences": <GitCompare size={20} />,
    "differences": <GitCompare size={20} />,
    "similarities": <Layers size={20} />,
    "common themes": <Layers size={20} />,

    // Research
    "research gaps": <Search size={20} />,
    "future research directions": <Compass size={20} />,
    "future work": <Compass size={20} />,
    "limitations": <AlertTriangle size={20} />,

    // Paper Summary
    "key contributions": <Target size={20} />,
    "methodology": <Cpu size={20} />,
    "main findings": <BarChart3 size={20} />,
    "results": <BarChart3 size={20} />,
    "practical applications": <Lightbulb size={20} />,

    // Recommendations
    "recommendations": <Lightbulb size={20} />,
    "next steps": <ArrowRight size={20} />,

    // Beginner Mode
    "simple explanation": <GraduationCap size={20} />,
    "key concepts": <BookOpen size={20} />,
    "takeaways": <Bookmark size={20} />,
};

export default function MarkdownRenderer({
    content,
}: MarkdownRendererProps) {

    const renderHeading = (children: ReactNode) => {

        const title = String(children).trim();

        const normalized = title.trim().toLowerCase().replace(/[:.]/g, "");

        const icon =
            headingIcons[normalized] ??
            <FileText size={20} />;

        return (
            <div className="ai-section-heading">
                {icon}
                <h2>{title}</h2>
            </div>
        );
    };

    return (
        <div className="markdown-content">
            <ReactMarkdown
                components={{
                    h1: ({ children }) => renderHeading(children),

                    h2: ({ children }) => renderHeading(children),

                    h3: ({ children }) => renderHeading(children),

                    ul: ({ children }) => (
                        <ul className="ai-list">
                            {children}
                        </ul>
                    ),

                    ol: ({ children }) => (
                        <ol className="ai-list">
                            {children}
                        </ol>
                    ),

                    li: ({ children }) => (
                        <li className="ai-list-item">
                            {children}
                        </li>
                    ),

                    p: ({ children }) => (
                        <p className="ai-paragraph">
                            {children}
                        </p>
                    ),

                    strong: ({ children }) => (
                        <strong className="ai-strong">
                            {children}
                        </strong>
                    ),

                    blockquote: ({ children }) => (
                        <blockquote className="ai-blockquote">
                            {children}
                        </blockquote>
                    ),

                    code: ({ children }) => (
                        <code className="ai-code">
                            {children}
                        </code>
                    ),
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
}