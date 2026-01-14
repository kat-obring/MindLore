export interface Topic {
  id: string;
  title: string;
  detail: string;
  suggestions: string[];
  selectedSuggestionIndex?: number;
}

export interface StructuredSuggestion {
  angle: string;
  hook: string;
  example: string;
  boundary: string;
  close: string;
  question: string;
}
