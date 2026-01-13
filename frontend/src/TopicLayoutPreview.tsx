import React, { useState } from "react";
import { colors, spacing, radius } from "./design/tokens";

export interface Topic {
  id: string;
  title: string;
  detail: string;
  suggestions: string[];
  selectedSuggestionIndex?: number;
}

const defaultTopics: Topic[] = [];

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

interface TopicLayoutPreviewProps {
  topics?: Topic[];
}

interface TopicEntryProps {
  onSubmit?: (title: string) => boolean;
  validationMessage?: string | null;
}

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

interface TopicListProps {
  topics: Topic[];
  selectedId?: string;
  onSelect: (id: string | undefined) => void;
  onGenerateSuggestions: (id: string) => void;
  onSelectSuggestion: (topicId: string, index: number) => void;
  isGenerating?: string | null;
}

function TopicList({
  topics,
  selectedId,
  onSelect,
  onGenerateSuggestions,
  onSelectSuggestion,
  isGenerating,
}: TopicListProps) {
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
              onClick={() =>
                onSelect(topic.id === selectedId ? undefined : topic.id)
              }
              style={topicButtonStyle}
            >
              {topic.title}
            </button>

            {isSelected && (
              <>
                {topic.suggestions.length === 0 ? (
                  <button
                    type="button"
                    disabled={isGenerating === topic.id}
                    onClick={() => onGenerateSuggestions(topic.id)}
                    style={{
                      ...entryButtonStyle,
                      alignSelf: "flex-start",
                      opacity: isGenerating === topic.id ? 0.5 : 1,
                    }}
                  >
                    {isGenerating === topic.id
                      ? "Generating..."
                      : "Generate Suggestions"}
                  </button>
                ) : (
                  <div style={{ display: "flex", gap: spacing.sm, flexWrap: "wrap" }}>
                    {topic.suggestions.map((suggestion, index) => {
                      const isSuggestionSelected =
                        topic.selectedSuggestionIndex === index;
                      return (
                        <button
                          key={index}
                          type="button"
                          onClick={() => onSelectSuggestion(topic.id, index)}
                          style={{
                            padding: `${spacing.xs} ${spacing.sm}`,
                            borderRadius: radius.sm,
                            border: `1px solid ${isSuggestionSelected ? colors.turquoise : colors.charcoal}`,
                            backgroundColor: isSuggestionSelected
                              ? colors.turquoise
                              : colors.champagne,
                            color: isSuggestionSelected ? "white" : "inherit",
                            cursor: "pointer",
                            fontSize: "0.8rem",
                          }}
                        >
                          {/* Use the first line as the button name, or just Outline A/B/C */}
                          {suggestion.split("\n")[0] || `Suggestion ${index + 1}`}
                        </button>
                      );
                    })}
                  </div>
                )}
                <div
                  data-testid={`topic-detail-${topic.id}`}
                  style={{
                    border: `1px dashed ${colors.gunmetal}`,
                    borderRadius: radius.md,
                    minHeight: "120px",
                    padding: spacing.sm,
                    backgroundColor: colors.ivory,
                    whiteSpace: "pre-wrap",
                  }}
                >
                  {topic.selectedSuggestionIndex !== undefined
                    ? topic.suggestions[topic.selectedSuggestionIndex]
                    : topic.detail}
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
  const [selectedId, setSelectedId] = useState<string | undefined>(undefined);
  const [validationMessage, setValidationMessage] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<string | null>(null);

  const hasTopics = topicItems.length > 0;

  const handleGenerateSuggestions = async (id: string) => {
    const topic = topicItems.find((t) => t.id === id);
    if (!topic) return;

    setIsGenerating(id);
    try {
      const response = await fetch("/api/suggestions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic.title }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate suggestions");
      }

      const data = await response.json();
      setTopicItems((prev) =>
        prev.map((t) =>
          t.id === id ? { ...t, suggestions: data.suggestions } : t,
        ),
      );
    } catch (error) {
      console.error(error);
      // For now, we just log the error. In a real app, we'd show a UI message.
    } finally {
      setIsGenerating(null);
    }
  };

  const handleSelectSuggestion = (topicId: string, index: number) => {
    setTopicItems((prev) =>
      prev.map((t) =>
        t.id === topicId ? { ...t, selectedSuggestionIndex: index } : t,
      ),
    );
  };

  const handleAddTopic = (title: string) => {
    const trimmed = title.trim();
    if (!trimmed) {
      setValidationMessage("Topic can not be blank");
      return false;
    }
    if (trimmed.length > 120) {
      setValidationMessage("Topic must be 120 characters or fewer");
      return false;
    }
    const normalized = trimmed.toLowerCase();
    const hasDuplicate = topicItems.some(
      (topic) => topic.title.trim().toLowerCase() === normalized,
    );
    if (hasDuplicate) {
      setValidationMessage("Topic already exists");
      return false;
    }

    const newTopic: Topic = {
      id: crypto.randomUUID(),
      title: trimmed,
      detail: "",
      suggestions: [],
    };
    setTopicItems((prev) => [newTopic, ...prev]);
    setSelectedId((prev) => prev);
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
          onGenerateSuggestions={handleGenerateSuggestions}
          onSelectSuggestion={handleSelectSuggestion}
          isGenerating={isGenerating}
        />
      ) : (
        <p>No saved topics</p>
      )}
    </>
  );
}

export default TopicLayoutPreview;
