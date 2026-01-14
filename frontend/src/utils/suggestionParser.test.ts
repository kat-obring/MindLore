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

    it("should extract all remaining fields (example, boundary, close, question)", () => {
      const raw = `### Outline A: The Tactical Approach

* **Hook:** This is the hook content
* **Example:** This is the example content
* **Boundary:** This is the boundary content
* **Close:** This is the close content
* **Question:** This is the question content`;

      const result = parseSuggestion(raw);

      expect(result.example).toBe("This is the example content");
      expect(result.boundary).toBe("This is the boundary content");
      expect(result.close).toBe("This is the close content");
      expect(result.question).toBe("This is the question content");
    });

    it("should handle missing fields gracefully", () => {
      const raw = `### Outline A: The Tactical Approach

* **Hook:** This is the hook content`;

      const result = parseSuggestion(raw);

      expect(result.angle).toBe("The Tactical Approach");
      expect(result.hook).toBe("This is the hook content");
      expect(result.example).toBe("");
      expect(result.boundary).toBe("");
      expect(result.close).toBe("");
      expect(result.question).toBe("");
    });
  });
});
