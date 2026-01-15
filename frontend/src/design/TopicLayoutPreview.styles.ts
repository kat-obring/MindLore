import { colors, spacing, radius } from "./tokens";

export const topicButtonStyle = {
  textAlign: "left",
  padding: spacing.xs,
  borderRadius: radius.sm,
  border: "none",
  background: "transparent",
  cursor: "pointer",
  fontWeight: 600,
  color: colors.midnight,
} as const;

export const entryContainerStyle = {
  display: "flex",
  flexDirection: "column",
  gap: spacing.xs,
  alignItems: "stretch",
  marginBottom: spacing.sm,
} as const;

export const entryRowStyle = {
  display: "flex",
  gap: spacing.sm,
  alignItems: "center",
} as const;

export const entryInputStyle = {
  flex: 1,
  padding: spacing.xs,
  borderRadius: radius.sm,
  border: `1px solid ${colors.charcoal}`,
} as const;

export const entryButtonStyle = {
  padding: `${spacing.xs} ${spacing.sm}`,
  borderRadius: radius.sm,
  border: `1px solid ${colors.charcoal}`,
  backgroundColor: colors.champagne,
  cursor: "pointer",
} as const;

export const suggestionDetailStyle = {
  display: "flex",
  flexDirection: "column",
  gap: spacing.xs,
  backgroundColor: colors.champagne,
  border: `1px solid ${colors.turquoise}`,
  borderRadius: radius.md,
  padding: spacing.sm,
} as const;

export const suggestionFieldStyle = {
  display: "flex",
  gap: spacing.xs,
  alignItems: "flex-start",
} as const;

export const suggestionLabelStyle = {
  minWidth: "90px",
  fontWeight: 700,
  color: colors.gunmetal,
} as const;

export const suggestionValueStyle = {
  color: colors.charcoal,
  lineHeight: 1.4,
} as const;
