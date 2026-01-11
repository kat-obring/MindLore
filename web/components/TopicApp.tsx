"use client";

import React, { FormEvent, useEffect, useState } from "react";

export type Idea = {
  id: number;
  title: string;
  status?: string;
};

type TopicAppProps = {
  apiBase?: string;
};

export function TopicApp({ apiBase }: TopicAppProps) {
  const base = apiBase ?? process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [suggestionsByIdea, setSuggestionsByIdea] = useState<Record<number, string[]>>({});

  useEffect(() => {
    let active = true;
    fetch(`${base}/ideas`)
      .then((res) => res.json())
      .then((data: Idea[]) => {
        if (active) setIdeas(data);
      })
      .catch(() => {
        if (active) setError("Failed to load ideas");
      });
    return () => {
      active = false;
    };
  }, [base]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!title.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${base}/ideas`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });
      if (!res.ok) throw new Error("Failed to create");
      const created: Idea = await res.json();
      setIdeas((prev) => [...prev, { ...created, status: created.status ?? "topic_saved" }]);
      setTitle("");
    } catch (err) {
      setError("Failed to create idea");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="New idea"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Saving..." : "Add Idea"}
        </button>
      </form>

      {error && <p role="alert">{error}</p>}

      <ul aria-label="ideas">
        {ideas.map((idea) => (
          <li key={idea.id}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <strong>{idea.title}</strong>
              <button
                type="button"
                aria-expanded={selectedId === idea.id}
                onClick={() => setSelectedId((current) => (current === idea.id ? null : idea.id))}
              >
                {selectedId === idea.id ? "Close" : `Open ${idea.title}`}
              </button>
            </div>
            {selectedId === idea.id && (
              <section aria-label={`details for ${idea.title}`}>
                <h3>{idea.title}</h3>
                <p>State: {idea.status ?? "unknown"}</p>
                <button
                  type="button"
                  onClick={async () => {
                    try {
                      const res = await fetch(`${base}/ideas/${idea.id}/angles`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ styleGuideName: "ideas_prompt" }),
                      });
                      if (!res.ok) throw new Error("Failed to request angles");
                      const data = (await res.json()) as string[];
                      setSuggestionsByIdea((prev) => ({ ...prev, [idea.id]: data }));
                    } catch {
                      // keep silent for now; could set error state
                    }
                  }}
                >
                  Send
                </button>
                {suggestionsByIdea[idea.id]?.length ? (
                  <div aria-label="suggestions" role="list">
                    {suggestionsByIdea[idea.id].map((suggestion, idx) => (
                      <div
                        key={idx}
                        role="listitem"
                        style={{
                          border: "1px solid #ccc",
                          borderRadius: "6px",
                          padding: "0.5rem",
                          marginTop: "0.5rem",
                        }}
                      >
                        {suggestion}
                      </div>
                    ))}
                  </div>
                ) : null}
              </section>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
