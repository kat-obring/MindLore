import React from "react";
import { act, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { TopicApp } from "../components/TopicApp";

function mockFetchSequence(responses: Array<{ status?: number; json: any }>) {
  let call = 0;
  vi.stubGlobal("fetch", vi.fn(async (url: string, options?: RequestInit) => {
    const current = responses[Math.min(call, responses.length - 1)];
    call += 1;
    return {
      ok: (current.status ?? 200) < 300,
      status: current.status ?? 200,
      json: async () => (typeof current.json === "function" ? current.json({ url, options }) : current.json),
    } as Response;
  }));
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
});
