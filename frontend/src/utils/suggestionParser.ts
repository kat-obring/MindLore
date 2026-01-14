import { StructuredSuggestion } from "../types";

export function parseSuggestion(raw: string): StructuredSuggestion {
  const extractField = (field: string) => {
    const regex = new RegExp(`\\*\\*${field}:\\*\\*\\s*(.*)`);
    const match = raw.match(regex);
    return match ? match[1].trim() : "";
  };

  const angleMatch = raw.match(/### Outline [A-Z]:\s*(.*)/);

  return {
    angle: angleMatch ? angleMatch[1].trim() : "",
    hook: extractField("Hook"),
    example: extractField("Example"),
    boundary: extractField("Boundary"),
    close: extractField("Close"),
    question: extractField("Question"),
  };
}
