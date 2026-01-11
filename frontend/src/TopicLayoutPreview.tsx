import React, { useState } from "react";
import { colors, spacing, radius } from "./design/tokens";

interface Topic {
  id: string;
  title: string;
  detail: string;
  suggestions: string[];
}

const topics: Topic[] = [
  {
    id: "topic-1",
    title: "Topic 1",
    detail: "Topic 1 detail",
    suggestions: ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
  },
  {
    id: "topic-2",
    title: "Topic 2",
    detail: "Topic 2 detail",
    suggestions: ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
  },
  {
    id: "topic-3",
    title: "Topic 3",
    detail: "Topic 3 detail",
    suggestions: ["Suggestion 1", "Suggestion 2", "Suggestion 3"],
  },
];

function TopicLayoutPreview() {
  const [selectedId, setSelectedId] = useState(topics[0]?.id);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: spacing.sm }}>
      {topics.map((topic) => {
        const isSelected = topic.id === selectedId;
        return (
          <article
            key={topic.id}
            data-testid={`topic-card-${topic.id}`}
            style={{
              border: `1px solid ${isSelected ? colors.turquoise : colors.charcoal}`,
              borderRadius: radius.md,
              backgroundColor: isSelected ? colors.ivory : "transparent",
              padding: spacing.sm,
              display: "flex",
              flexDirection: "column",
              gap: spacing.sm,
            }}
          >
            <button
              onClick={() => setSelectedId(topic.id)}
              style={{
                textAlign: "left",
                padding: spacing.xs,
                borderRadius: radius.sm,
                border: "none",
                background: "transparent",
                cursor: "pointer",
                fontWeight: 600,
                color: colors.midnight,
              }}
            >
              {topic.title}
            </button>

            {isSelected && (
              <>
                <div style={{ display: "flex", gap: spacing.sm }}>
                  {topic.suggestions.map((suggestion, index) => (
                    <button
                      key={suggestion}
                      type="button"
                      style={{
                        padding: `${spacing.xs} ${spacing.sm}`,
                        borderRadius: radius.sm,
                        border: `1px solid ${colors.charcoal}`,
                        backgroundColor: colors.champagne,
                        cursor: "pointer",
                      }}
                    >
                      {`Suggestion ${index + 1}`}
                    </button>
                  ))}
                </div>
                <div
                  style={{
                    border: `1px dashed ${colors.gunmetal}`,
                    borderRadius: radius.md,
                    minHeight: "120px",
                    padding: spacing.sm,
                    backgroundColor: colors.ivory,
                  }}
                >
                  {topic.detail}
                </div>
              </>
            )}
          </article>
        );
      })}
    </div>
  );
}

export default TopicLayoutPreview;
