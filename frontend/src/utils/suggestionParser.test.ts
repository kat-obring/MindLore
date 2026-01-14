import { describe, it, expect } from "vitest";
import { parseSuggestion } from "./suggestionParser";

describe("suggestionParser", () => {
  describe("parseSuggestion", () => {
    it("should extract the angle name from the outline header", () => {
      const raw = `### Outline A: The Tactical Approach

* **Hook:** Some hook content`;
      
      const result = parseSuggestion(raw);
      
      expect(result.angle).toBe("The Tactical Approach");
    });
  });
});
