import { useState } from "react";

type PromptTemplatesProps = {
  onSelect: (prompt: string) => void;
};

const templates = [
  {
    icon: "📝",
    title: "Executive Summary",
    description: "Summarize the key contributions of the selected papers.",
    prompt: "Summarize the main contributions of these research papers.",
  },
  {
    icon: "⚖️",
    title: "Compare Papers",
    description:
      "Compare objectives, methodology, datasets and results.",
    prompt:
      "Compare these research papers in terms of objectives, methodology, datasets, and results.",
  },
  {
    icon: "🔍",
    title: "Research Gaps",
    description:
      "Identify limitations and propose future research directions.",
    prompt:
      "Identify the research gaps and suggest potential future research directions.",
  },
  {
    icon: "🧪",
    title: "Methodology",
    description:
      "Compare the strengths and weaknesses of each approach.",
    prompt:
      "Compare the methodologies used in these papers and explain their strengths and weaknesses.",
  },
  {
    icon: "📚",
    title: "Literature Review",
    description:
      "Generate a concise literature review from the selected papers.",
    prompt:
      "Write a concise literature review based on these selected papers.",
  },
  {
    icon: "💡",
    title: "Explain Simply",
    description:
      "Explain the papers in beginner-friendly language.",
    prompt:
      "Explain the key concepts from these papers in simple language suitable for a beginner.",
  },
];

function PromptTemplates({
  onSelect,
}: PromptTemplatesProps) {

    const [selectedTemplate, setSelectedTemplate] =useState<string | null>(null);

  return (
    <div className="prompt-templates">
      <div className="prompt-header">
        <h3>✨ Quick Prompts</h3>
        <p>
            Select a template to instantly generate a high-quality research prompt.
        </p>
    </div>

      <div className="template-grid">
            {templates.map((template) => (
                <button
                    key={template.title}
                    className={`template-card ${
                        selectedTemplate === template.title ? "active" : ""
                    }`}
                    onClick={() => {
                        setSelectedTemplate(template.title);
                        onSelect(template.prompt);
                    }}
                >
                    <div className="template-icon">
                        {template.icon}
                    </div>

                    <div className="template-title-row">
                        <h4>{template.title}</h4>

                        {selectedTemplate === template.title && (
                            <span className="selected-badge">
                                ✓ Selected
                            </span>
                        )}
                    </div>

                    <p>{template.description}</p>
                </button>
            ))}
        </div>
    </div>
  );
}

export default PromptTemplates;