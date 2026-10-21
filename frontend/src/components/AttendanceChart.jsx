import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = {
  primary: "#173142",
  border: "#DCE4E9",
  muted: "#607D8B",
  text: "#1F2937",
  background: "#F3F6F8",
};

export default function AttendanceChart({ data = [] }) {
  // data: [{ course_code, present, absent, late, excused }]
  return (
    <div
      style={{
        background: "#FFFFFF",
        border: `1px solid ${COLORS.border}`,
        borderRadius: 12,
        padding: 20,
      }}
    >
      <h3 style={{ margin: "0 0 16px", color: COLORS.text, fontSize: 16 }}>
        Attendance Overview
      </h3>

      {data.length === 0 ? (
        <p style={{ color: COLORS.muted, textAlign: "center", padding: 40 }}>
          No attendance data available.
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
            <XAxis dataKey="course_code" tick={{ fill: COLORS.muted, fontSize: 12 }} />
            <YAxis tick={{ fill: COLORS.muted, fontSize: 12 }} />
            <Tooltip
              contentStyle={{
                background: "#FFFFFF",
                border: `1px solid ${COLORS.border}`,
                borderRadius: 8,
                color: COLORS.text,
              }}
            />
            <Bar dataKey="present" fill={COLORS.primary} radius={[4, 4, 0, 0]} />
            <Bar dataKey="absent" fill="#C0392B" radius={[4, 4, 0, 0]} />
            <Bar dataKey="late" fill="#E67E22" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
