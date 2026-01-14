export interface StructuredSuggestion {
  angle: string;
  hook: string;
}

export function parseSuggestion(raw: string): StructuredSuggestion {
  const angleMatch = raw.match(/### Outline [A-Z]:\s*(.*)/);
  const hookMatch = raw.match(/\*\*Hook:\*\*\s*(.*)/);
  
  return {
    angle: angleMatch ? angleMatch[1].trim() : "",
    hook: hookMatch ? hookMatch[1].trim() : "",
  };
}
