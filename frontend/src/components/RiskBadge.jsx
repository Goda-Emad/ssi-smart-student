const LEVEL_STYLES = {
  High:   { background: "#FDECEA", color: "#C0392B", border: "#F5C6C0" },
  Medium: { background: "#FFF4E5", color: "#B9770E", border: "#F5DDB8" },
  Low:    { background: "#E8F5E9", color: "#2E7D32", border: "#C8E6C9" },
};

export default function RiskBadge({ level = "Low", score = null }) {
  const style = LEVEL_STYLES[level] || LEVEL_STYLES.Low;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "4px 12px",
        borderRadius: 999,
        fontSize: 13,
        fontWeight: 600,
        background: style.background,
        color: style.color,
        border: `1px solid ${style.border}`,
        whiteSpace: "nowrap",
      }}
    >
      {level}
      {score !== null && <span style={{ opacity: 0.75 }}>({score}%)</span>}
    </span>
  );
}
