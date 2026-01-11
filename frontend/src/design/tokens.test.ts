import { describe, expect, it } from "vitest";

import { colors, fonts, radius, spacing } from "./tokens";

describe("design tokens", () => {
  it("exposes palette tokens from the style guide", () => {
    expect(colors).toMatchObject({
      copper: "#B87333",
      turquoise: "#30D5C8",
      verdigris: "#43B5A0",
      verdigrisSoft: "#679267",
      charcoal: "#4A4A48",
      gunmetal: "#2C2C2C",
      ivory: "#F9F6EF",
      champagne: "#E8D8C3",
      amber: "#FFBF00",
      brass: "#D4A017",
      midnight: "#003366",
      prussian: "#1F4E5F",
    });
  });

  it("exposes typography stacks for headings and body", () => {
    expect(fonts).toEqual({
      heading: "'Lora', serif",
      body: "'Inter', 'Inter Variable', system-ui, -apple-system, sans-serif",
    });
  });

  it("exposes spacing scale in rems", () => {
    expect(spacing).toEqual({
      xs: "0.25rem",
      sm: "0.5rem",
      md: "0.75rem",
      base: "1rem",
      lg: "1.5rem",
      xl: "2rem",
    });
  });

  it("exposes corner radius tokens", () => {
    expect(radius).toEqual({
      sm: "4px",
      md: "8px",
    });
  });
});
