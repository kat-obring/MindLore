import React from "react";
import TopicLayoutPreview from "./TopicLayoutPreview";
import { colors, spacing } from "./design/tokens";

function App() {
  return (
    <div
      style={{
        backgroundColor: colors.ivory,
        color: colors.charcoal,
        minHeight: "100vh",
        padding: spacing.lg,
        fontFamily: "Inter, system-ui, -apple-system, sans-serif",
      }}
    >
      <header style={{ marginBottom: spacing.lg, textAlign: "center" }}>
        <h1 style={{ fontFamily: "Lora, serif", margin: 0 }}>MindLore</h1>
        <p style={{ margin: 0, color: colors.gunmetal }}>
          Topic layout preview
        </p>
      </header>
      <TopicLayoutPreview />
    </div>
  );
}

export default App;
