import React, { useState } from "react";
import { colors, spacing, radius } from "./design/tokens";

export interface Topic {
  id: string;
  title: string;
  detail: string;
  suggestions: string[];
}

const defaultTopics: Topic[] = [];

const detailMinHeight = "120px";

const listStyle = {
  display: "flex",
  flexDirection: "column",
  gap: spacing.sm,
} as const;

const cardBaseStyle = {
  borderRadius: radius.md,
  padding: spacing.sm,
  display: "flex",
  flexDirection: "column",
  gap: spacing.sm,
} as const;

const selectedCardStyle = {
  border: `1px solid ${colors.turquoise}`,
  backgroundColor: colors.ivory,
} as const;

const unselectedCardStyle = {
  border: `1px solid ${colors.charcoal}`,
  backgroundColor: "transparent",
} as const;

const topicButtonStyle = {
  textAlign: "left",
  padding: spacing.xs,
  borderRadius: radius.sm,
  border: "none",
  background: "transparent",
  cursor: "pointer",
  fontWeight: 600,
  color: colors.midnight,
} as const;

const suggestionsRowStyle = {
  display: "flex",
  gap: spacing.sm,
} as const;

const suggestionButtonStyle = {
  padding: `${spacing.xs} ${spacing.sm}`,
  borderRadius: radius.sm,
  border: `1px solid ${colors.charcoal}`,
  backgroundColor: colors.champagne,
  cursor: "pointer",
} as const;

const detailPanelStyle = {
  border: `1px dashed ${colors.gunmetal}`,
  borderRadius: radius.md,
  minHeight: detailMinHeight,
  padding: spacing.sm,
  backgroundColor: colors.ivory,
} as const;

const entryContainerStyle = {
  display: "flex",
  flexDirection: "column",
  gap: spacing.xs,
  alignItems: "stretch",
  marginBottom: spacing.sm,
} as const;

const entryRowStyle = {
  display: "flex",
  gap: spacing.sm,
  alignItems: "center",
} as const;

const entryInputStyle = {
  flex: 1,
  padding: spacing.xs,
  borderRadius: radius.sm,
  border: `1px solid ${colors.charcoal}`,
} as const;

const entryButtonStyle = {
  padding: `${spacing.xs} ${spacing.sm}`,
  borderRadius: radius.sm,
  border: `1px solid ${colors.charcoal}`,
  backgroundColor: colors.champagne,
  cursor: "pointer",
} as const;

type TopicLayoutPreviewProps = {
  topics?: Topic[];
};

type TopicEntryProps = {
  onSubmit?: (title: string) => boolean;
  validationMessage?: string | null;
};

function TopicEntry({ onSubmit, validationMessage }: TopicEntryProps) {
  const [value, setValue] = useState("");

  const handleSubmit = () => {
    const didSubmit = onSubmit?.(value) ?? false;
    if (didSubmit) {
      setValue("");
    }
  };

  return (
    <div style={entryContainerStyle}>
      <div style={entryRowStyle}>
        <input
          aria-label="Topic"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              handleSubmit();
            }
          }}
          style={{
            ...entryInputStyle,
            ...(validationMessage
              ? {
                  border: `1px solid ${colors.copper}`,
                  outlineColor: colors.copper,
                }
              : {}),
          }}
        />
        <button
          type="button"
          onClick={handleSubmit}
          style={entryButtonStyle}
        >
          Save
        </button>
      </div>
      {validationMessage && (
        <p style={{ margin: 0, color: colors.copper }}>{validationMessage}</p>
      )}
    </div>
  );
}

type TopicListProps = {
  topics: Topic[];
  selectedId?: string;
  onSelect: (id: string) => void;
};

function TopicList({ topics, selectedId, onSelect }: TopicListProps) {
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
              onClick={() => onSelect(topic.id === selectedId ? undefined : topic.id)}
              style={topicButtonStyle}
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

function TopicLayoutPreview({
  topics: initialTopics = defaultTopics,
}: TopicLayoutPreviewProps) {
  const [topicItems, setTopicItems] = useState(initialTopics);
  const [selectedId, setSelectedId] = useState(initialTopics[0]?.id);
  const [validationMessage, setValidationMessage] = useState<string | null>(null);

  const hasTopics = topicItems.length > 0;

  const handleAddTopic = (title: string) => {
    const trimmed = title.trim();
    if (!trimmed) {
      setValidationMessage("Topic can not be blank");
      return false;
    }

    const newTopic: Topic = {
      id: `topic-${Date.now()}`,
      title,
      detail: "",
      suggestions: [],
    };
    setTopicItems((prev) => [newTopic, ...prev]);
    setSelectedId(newTopic.id);
    setValidationMessage(null);
    return true;
  };

  return (
    <>
      <TopicEntry
        onSubmit={handleAddTopic}
        validationMessage={validationMessage}
      />
      {hasTopics ? (
        <TopicList
          topics={topicItems}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />
      ) : (
        <p>No saved topics</p>
      )}
    </>
  );
}

export default TopicLayoutPreview;
