import React from "react";
import { render, screen, fireEvent, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import TopicLayoutPreview from "./TopicLayoutPreview";
import { Topic } from "./types";

const sampleTopics: Topic[] = [
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

describe("TopicLayoutPreview", () => {
  it("shows a list of topics and updates selection", () => {
    render(<TopicLayoutPreview topics={sampleTopics} />);

    const topic1 = screen.getByRole("button", { name: /topic 1/i });
    const topic2 = screen.getByRole("button", { name: /topic 2/i });
    const topic3 = screen.getByRole("button", { name: /topic 3/i });

    expect(topic1).toBeInTheDocument();
    expect(topic2).toBeInTheDocument();
    expect(topic3).toBeInTheDocument();

    fireEvent.click(topic1);
    expect(screen.getByText(/Topic 1 detail/i)).toBeInTheDocument();

    fireEvent.click(topic2);
    expect(screen.getByText(/Topic 2 detail/i)).toBeInTheDocument();
  });

  it("renders three suggestion tabs for the selected topic", () => {
    render(<TopicLayoutPreview topics={sampleTopics} />);

    fireEvent.click(screen.getByRole("button", { name: /topic 1/i }));

    expect(
      screen.getByRole("button", { name: /suggestion 1/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /suggestion 2/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /suggestion 3/i }),
    ).toBeInTheDocument();
  });

  it("renders details inside the selected topic card, stacked vertically", () => {
    render(<TopicLayoutPreview topics={sampleTopics} />);

    fireEvent.click(screen.getByRole("button", { name: /topic 1/i }));
    const topic1Card = screen.getByTestId("topic-card-topic-1");
    expect(
      within(topic1Card).getByText(/Topic 1 detail/i),
    ).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /topic 2/i }));
    const topic2Card = screen.getByTestId("topic-card-topic-2");
    expect(
      within(topic2Card).getByText(/Topic 2 detail/i),
    ).toBeInTheDocument();
  });

  it('shows "No saved topics" when there are no topics', () => {
    const { container } = render(<TopicLayoutPreview topics={[]} />);
    expect(screen.getByText(/No saved topics/i)).toBeInTheDocument();
    expect(
      container.querySelector("[data-testid^='topic-card-']"),
    ).not.toBeInTheDocument();
  });

  it("shows the topic input above the topics list with a visible Save button", () => {
    render(<TopicLayoutPreview topics={sampleTopics} />);

    const topicInput = screen.getByRole("textbox");
    const saveButton = screen.getByRole("button", { name: /save/i });
    const firstTopicButton = screen.getByRole("button", { name: /topic 1/i });

    expect(topicInput).toBeInTheDocument();
    expect(saveButton).toBeInTheDocument();
    expect(
      topicInput.compareDocumentPosition(firstTopicButton) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it("pressing Enter saves a non-empty trimmed topic, clears the input, and prepends it", () => {
    const { container } = render(<TopicLayoutPreview topics={sampleTopics} />);

    const topicInput = screen.getByRole("textbox");

    fireEvent.change(topicInput, { target: { value: "  New Topic  " } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    const updatedCards = container.querySelectorAll(
      "[data-testid^='topic-card-']",
    );

    expect(updatedCards.length).toBe(sampleTopics.length + 1);
    expect(updatedCards[0]).toHaveTextContent("New Topic");
    expect((topicInput as HTMLInputElement).value).toBe("");
  });

  it("clicking Save performs the same save/clear/prepend behavior", () => {
    const { container } = render(<TopicLayoutPreview topics={sampleTopics} />);

    const topicInput = screen.getByRole("textbox");
    const saveButton = screen.getByRole("button", { name: /save/i });

    fireEvent.change(topicInput, { target: { value: "  Save Click Topic  " } });
    fireEvent.click(saveButton);

    const updatedCards = container.querySelectorAll(
      "[data-testid^='topic-card-']",
    );

    expect(updatedCards.length).toBe(sampleTopics.length + 1);
    expect(updatedCards[0]).toHaveTextContent("Save Click Topic");
    expect((topicInput as HTMLInputElement).value).toBe("");
  });

  it('shows "Topic can not be blank" for empty/whitespace submits, blocks save, and clears after success', () => {
    const { container } = render(<TopicLayoutPreview topics={[]} />);

    const topicInput = screen.getByRole("textbox");

    fireEvent.change(topicInput, { target: { value: "   " } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(
      screen.getByText(/Topic can not be blank/i),
    ).toBeInTheDocument();
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']").length,
    ).toBe(0);

    fireEvent.change(topicInput, { target: { value: "Valid Topic" } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(
      screen.queryByText(/Topic can not be blank/i),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText(/No saved topics/i),
    ).not.toBeInTheDocument();
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']").length,
    ).toBe(1);
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']")[0],
    ).toHaveTextContent("Valid Topic");
  });

  it("blocks submissions over 120 characters with a max-length message, clears after success", () => {
    const { container } = render(<TopicLayoutPreview topics={[]} />);

    const longText = "a".repeat(121);
    const topicInput = screen.getByRole("textbox");

    fireEvent.change(topicInput, { target: { value: longText } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(
      screen.getByText(/must be 120 characters or fewer/i),
    ).toBeInTheDocument();
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']").length,
    ).toBe(0);

    fireEvent.change(topicInput, { target: { value: "Short enough" } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(
      screen.queryByText(/must be 120 characters or fewer/i),
    ).not.toBeInTheDocument();
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']").length,
    ).toBe(1);
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']")[0],
    ).toHaveTextContent("Short enough");
  });

  it("blocks duplicate topics (case-insensitive, trimmed) with a duplicate message, clears after success", () => {
    const { container } = render(<TopicLayoutPreview topics={[]} />);
    const topicInput = screen.getByRole("textbox");

    fireEvent.change(topicInput, { target: { value: "First Topic" } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    fireEvent.change(topicInput, { target: { value: "  first topic  " } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(
      screen.getByText(/topic already exists/i),
    ).toBeInTheDocument();
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']").length,
    ).toBe(1);

    fireEvent.change(topicInput, { target: { value: "Second Topic" } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(
      screen.queryByText(/topic already exists/i),
    ).not.toBeInTheDocument();
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']").length,
    ).toBe(2);
    expect(
      container.querySelectorAll("[data-testid^='topic-card-']")[0],
    ).toHaveTextContent("Second Topic");
  });

  it("removes the empty state after adding a topic", () => {
    const { container } = render(<TopicLayoutPreview topics={[]} />);
    const topicInput = screen.getByRole("textbox");

    expect(screen.getByText(/No saved topics/i)).toBeInTheDocument();

    fireEvent.change(topicInput, { target: { value: "First Topic" } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    expect(screen.queryByText(/No saved topics/i)).not.toBeInTheDocument();
    const cards = container.querySelectorAll("[data-testid^='topic-card-']");
    expect(cards.length).toBe(1);
    expect(cards[0]).toHaveTextContent("First Topic");
  });

  it("newly added topics can be toggled open and closed via their title", () => {
    render(<TopicLayoutPreview topics={[]} />);
    const topicInput = screen.getByRole("textbox");

    fireEvent.change(topicInput, { target: { value: "Fresh Topic" } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    const card = screen.getByTestId(/topic-card-/i);
    expect(screen.queryByTestId(/topic-detail-/i)).not.toBeInTheDocument();

    const titleButton = within(card).getByRole("button", { name: /fresh topic/i });
    fireEvent.click(titleButton);
    expect(screen.getByTestId(/topic-detail-/i)).toBeInTheDocument();

    fireEvent.click(titleButton);
    expect(screen.queryByTestId(/topic-detail-/i)).not.toBeInTheDocument();
  });

  it("toggles a topic card open when closed and closed when open", () => {
    render(<TopicLayoutPreview topics={sampleTopics} />);

    const topic1Button = screen.getByRole("button", { name: /topic 1/i });
    const topic1Card = screen.getByTestId("topic-card-topic-1");

    fireEvent.click(topic1Button);
    expect(within(topic1Card).getByText(/Topic 1 detail/i)).toBeInTheDocument();

    fireEvent.click(topic1Button);
    expect(
      within(topic1Card).queryByText(/Topic 1 detail/i),
    ).not.toBeInTheDocument();

    fireEvent.click(topic1Button);
    expect(within(topic1Card).getByText(/Topic 1 detail/i)).toBeInTheDocument();
  });

  it("renders HTML-like topic titles as text (no execution/markup)", () => {
    const maliciousTitle = '<script>alert("xss")</script>';
    render(
      <TopicLayoutPreview
        topics={[
          {
            id: "topic-xss",
            title: maliciousTitle,
            detail: "Detail",
            suggestions: [],
          },
        ]}
      />,
    );

    expect(screen.getByText(maliciousTitle)).toBeInTheDocument();
  });

  it("shows a 'Generate Suggestions' button and updates suggestions on click", async () => {
    const mockSuggestions = [
      "### Outline A: Angle 1",
      "### Outline B: Angle 2",
      "### Outline C: Angle 3",
    ];
    const fetchSpy = vi.spyOn(window, "fetch").mockResolvedValue({
      ok: true,
      json: async () => ({ suggestions: mockSuggestions }),
    } as Response);

    render(
      <TopicLayoutPreview
        topics={[{ id: "1", title: "Test Topic", detail: "", suggestions: [] }]}
      />,
    );

    // Open the topic
    fireEvent.click(screen.getByRole("button", { name: /test topic/i }));

    const generateBtn = screen.getByRole("button", {
      name: /generate suggestions/i,
    });
    fireEvent.click(generateBtn);

    expect(fetchSpy).toHaveBeenCalledWith(
      "/api/suggestions",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ topic: "Test Topic" }),
      }),
    );

    // Check that suggestions are rendered
    expect(
      await screen.findByRole("button", { name: /outline a: angle 1/i }),
    ).toBeInTheDocument();
    expect(
      await screen.findByRole("button", { name: /outline b: angle 2/i }),
    ).toBeInTheDocument();
    expect(
      await screen.findByRole("button", { name: /outline c: angle 3/i }),
    ).toBeInTheDocument();

    fetchSpy.mockRestore();
  });
});
