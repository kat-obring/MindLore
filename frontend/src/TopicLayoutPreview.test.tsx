import React from "react";
import { render, screen, fireEvent, within } from "@testing-library/react";
import TopicLayoutPreview from "./TopicLayoutPreview";
import { describe, expect, it } from "vitest";

describe("TopicLayoutPreview", () => {
  it("shows a list of topics and updates selection", () => {
    render(<TopicLayoutPreview />);

    const topic1 = screen.getByRole("button", { name: /topic 1/i });
    const topic2 = screen.getByRole("button", { name: /topic 2/i });
    const topic3 = screen.getByRole("button", { name: /topic 3/i });

    expect(topic1).toBeInTheDocument();
    expect(topic2).toBeInTheDocument();
    expect(topic3).toBeInTheDocument();

    expect(screen.getByText(/Topic 1 detail/i)).toBeInTheDocument();

    fireEvent.click(topic2);
    expect(screen.getByText(/Topic 2 detail/i)).toBeInTheDocument();
  });

  it("renders three suggestion tabs for the selected topic", () => {
    render(<TopicLayoutPreview />);

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
    render(<TopicLayoutPreview />);

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

  it("renders nothing when no topics are provided", () => {
    const { container } = render(<TopicLayoutPreview topics={[]} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("shows the topic input above the topics list with a visible Save button", () => {
    render(<TopicLayoutPreview />);

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
    const { container } = render(<TopicLayoutPreview />);

    const topicInput = screen.getByRole("textbox");

    fireEvent.change(topicInput, { target: { value: "  New Topic  " } });
    fireEvent.keyDown(topicInput, { key: "Enter", code: "Enter" });

    const updatedCards = container.querySelectorAll(
      "[data-testid^='topic-card-']",
    );

    expect(updatedCards.length).toBeGreaterThan(3);
    expect(updatedCards[0]).toHaveTextContent("New Topic");
    expect((topicInput as HTMLInputElement).value).toBe("");
  });
});
