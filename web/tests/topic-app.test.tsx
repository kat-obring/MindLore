import React from "react";
import { act, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { TopicApp } from "../components/TopicApp";

function mockFetchSequence(responses: Array<{ status?: number; json: any }>) {
  let call = 0;
  const mock = vi.fn(async (url: string, options?: RequestInit) => {
    const current = responses[Math.min(call, responses.length - 1)];
    call += 1;
    return {
      ok: (current.status ?? 200) < 300,
      status: current.status ?? 200,
      json: async () =>
        typeof current.json === "function" ? current.json({ url, options }) : current.json,
    } as Response;
  });
  vi.stubGlobal("fetch", mock);
  return mock;
}

describe("TopicApp", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows existing ideas and allows adding a new one", async () => {
    mockFetchSequence([
      { json: [{ id: 1, title: "Existing" }] }, // initial GET /ideas
      {
        json: ({ options }) => {
          const body = options?.body ? JSON.parse(options.body as string) : {};
          return { id: 2, title: body.title };
        },
      }, // POST /ideas
    ]);

    render(<TopicApp apiBase="http://test/api" />);

    expect(await screen.findByText("Existing")).toBeInTheDocument();

    await userEvent.type(screen.getByLabelText(/title/i), "New Idea");

    await act(async () => {
      await userEvent.click(screen.getByRole("button", { name: /add idea/i }));
    });

    await waitFor(() => {
      expect(screen.getByText("New Idea")).toBeInTheDocument();
    });
  });

  it("expands a topic to show detail with status and send action", async () => {
    mockFetchSequence([{ json: [{ id: 1, title: "Topic 1", status: "topic_saved" }] }]);

    render(<TopicApp apiBase="http://test/api" />);

    expect(await screen.findByText("Topic 1")).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: /open topic 1/i }));

    const detail = await screen.findByLabelText(/details for topic 1/i);
    expect(within(detail).getByText(/state:\s*topic_saved/i)).toBeInTheDocument();
    expect(within(detail).getByRole("button", { name: /send/i })).toBeInTheDocument();
  });

  it("shows topic title and placeholder state when none provided", async () => {
    mockFetchSequence([{ json: [{ id: 2, title: "Untitled Topic" }] }]);

    render(<TopicApp apiBase="http://test/api" />);

    await userEvent.click(await screen.findByRole("button", { name: /open untitled topic/i }));

    const detail = await screen.findByLabelText(/details for untitled topic/i);
    expect(within(detail).getByText("Untitled Topic")).toBeInTheDocument();
    expect(within(detail).getByText(/state:\s*unknown/i)).toBeInTheDocument();
    expect(within(detail).getByRole("button", { name: /send/i })).toBeInTheDocument();
  });

  it("posts to angles endpoint with style guide and receives three suggestions on Send", async () => {
    const fetchMock = mockFetchSequence([
      { json: [{ id: 3, title: "Need ideas", status: "topic_saved" }] }, // GET /ideas
      { json: ["Opt A", "Opt B", "Opt C"] }, // POST /ideas/3/angles
    ]);

    render(<TopicApp apiBase="http://test/api" />);

    await userEvent.click(await screen.findByRole("button", { name: /open need ideas/i }));
    await userEvent.click(screen.getByRole("button", { name: /send/i }));

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledTimes(2);
    });
    expect(fetchMock.mock.calls[1]?.[0]).toBe("http://test/api/ideas/3/angles");
    const options = fetchMock.mock.calls[1]?.[1] as RequestInit;
    expect(options?.method).toBe("POST");
    expect(options?.headers).toMatchObject({ "Content-Type": "application/json" });
    const sentBody = options?.body ? JSON.parse(options.body as string) : {};
    expect(sentBody).toEqual({ styleGuideName: "ideas_prompt" });

    const detail = await screen.findByLabelText(/details for need ideas/i);
    expect(within(detail).getAllByRole("listitem")).toHaveLength(3);
    expect(within(detail).getByText("Opt A")).toBeInTheDocument();
    expect(within(detail).getByText("Opt B")).toBeInTheDocument();
    expect(within(detail).getByText("Opt C")).toBeInTheDocument();
  });

  it("renders returned suggestions as cards", async () => {
    mockFetchSequence([
      { json: [{ id: 4, title: "Card topic", status: "topic_saved" }] }, // GET /ideas
      { json: ["Card A", "Card B", "Card C"] }, // POST /ideas/4/angles
    ]);

    render(<TopicApp apiBase="http://test/api" />);

    await userEvent.click(await screen.findByRole("button", { name: /open card topic/i }));
    await userEvent.click(screen.getByRole("button", { name: /send/i }));

    const list = await screen.findByLabelText(/suggestions/i);
    const cards = within(list).getAllByRole("listitem");
    expect(cards).toHaveLength(3);
    expect(within(cards[0]).getByText("Card A")).toBeInTheDocument();
    expect(within(cards[1]).getByText("Card B")).toBeInTheDocument();
    expect(within(cards[2]).getByText("Card C")).toBeInTheDocument();
  });
});
