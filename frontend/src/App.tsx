import React from "react";
import TopicLayoutPreview from "./TopicLayoutPreview";
import { colors, spacing } from "./design/tokens";

const appShellStyle = {
  backgroundColor: colors.ivory,
  color: colors.charcoal,
  minHeight: "100vh",
  padding: spacing.lg,
  fontFamily: "Inter, system-ui, -apple-system, sans-serif",
} as const;

const headerStyle = {
  marginBottom: spacing.lg,
  textAlign: "center",
} as const;

const titleStyle = {
  fontFamily: "Lora, serif",
  margin: 0,
} as const;

const subtitleStyle = {
  margin: 0,
  color: colors.gunmetal,
} as const;

function App() {
  return (
    <div style={appShellStyle}>
      <header style={headerStyle}>
        <h1 style={titleStyle}>MindLore</h1>
        <p style={subtitleStyle}>Topic layout preview</p>
      </header>
      <TopicLayoutPreview />
    </div>
  );
}

export default App;
