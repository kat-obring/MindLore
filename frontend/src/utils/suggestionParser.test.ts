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

    it("should extract the hook content", () => {
      const raw = `### Outline A: The Tactical Approach

* **Hook:** This is the hook content
* **Example:** Some example`;

      const result = parseSuggestion(raw);

      expect(result.hook).toBe("This is the hook content");
    });
  });
});
