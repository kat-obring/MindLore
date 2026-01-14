import { beforeEach, describe, expect, it, vi } from "vitest";

describe("main entry styling", () => {
  beforeEach(() => {
    document.body.innerHTML = '<div id="root"></div>';
    vi.resetModules();
  });

  it("applies the base styling class to the body", async () => {
    await import("./main");

    expect(document.body.classList.contains("mindlore-root")).toBe(true);
  });
});
