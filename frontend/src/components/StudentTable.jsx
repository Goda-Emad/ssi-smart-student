import RiskBadge from "./RiskBadge";

const COLORS = {
  primary: "#173142",
  background: "#F3F6F8",
  border: "#DCE4E9",
  muted: "#607D8B",
  text: "#1F2937",
};

export default function StudentTable({ students = [], onSelect = null }) {
  if (!students.length) {
    return (
      <div
        style={{
          background: "#FFFFFF",
          border: `1px solid ${COLORS.border}`,
          borderRadius: 12,
          padding: 40,
          textAlign: "center",
          color: COLORS.muted,
        }}
      >
        No students found.
      </div>
    );
  }

  return (
    <div
      style={{
        background: "#FFFFFF",
        border: `1px solid ${COLORS.border}`,
        borderRadius: 12,
        overflow: "hidden",
      }}
    >
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
        <thead>
          <tr style={{ background: COLORS.background }}>
            {["Student ID", "Name", "Faculty", "GPA", "Attendance", "Risk", ""].map(
              (h) => (
                <th
                  key={h}
                  style={{
                    textAlign: "left",
                    padding: "12px 16px",
                    color: COLORS.muted,
                    fontWeight: 600,
                    fontSize: 12,
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    borderBottom: `1px solid ${COLORS.border}`,
                  }}
                >
                  {h}
                </th>
              )
            )}
          </tr>
        </thead>
        <tbody>
          {students.map((s) => (
            <tr
              key={s.student_id}
              style={{
                borderBottom: `1px solid ${COLORS.border}`,
                transition: "background 0.15s",
                cursor: onSelect ? "pointer" : "default",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = COLORS.background)}
              onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
              onClick={() => onSelect && onSelect(s)}
            >
              <td style={{ padding: "12px 16px", color: COLORS.text, fontWeight: 500 }}>
                {s.student_id}
              </td>
              <td style={{ padding: "12px 16px", color: COLORS.text }}>{s.full_name}</td>
              <td style={{ padding: "12px 16px", color: COLORS.muted }}>{s.faculty}</td>
              <td style={{ padding: "12px 16px", color: COLORS.text }}>
                {Number(s.gpa).toFixed(2)}
              </td>
              <td style={{ padding: "12px 16px", color: COLORS.text }}>
                {Number(s.attendance_rate).toFixed(1)}%
              </td>
              <td style={{ padding: "12px 16px" }}>
                <RiskBadge level={s.risk_level} score={s.risk_score} />
              </td>
              <td style={{ padding: "12px 16px", textAlign: "right" }}>
                {onSelect && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelect(s);
                    }}
                    style={{
                      background: COLORS.primary,
                      color: "#FFFFFF",
                      border: "none",
                      padding: "6px 12px",
                      borderRadius: 6,
                      fontSize: 12,
                      cursor: "pointer",
                    }}
                  >
                    View
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
