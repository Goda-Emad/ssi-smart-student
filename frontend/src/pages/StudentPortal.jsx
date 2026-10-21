import { useEffect, useState } from "react";
import api from "../services/api";
import logo from "../assets/logo.png";
import SmartIDCard from "../components/SmartIDCard";
import AttendanceChart from "../components/AttendanceChart";
import RiskBadge from "../components/RiskBadge";

const COLORS = {
  primary: "#173142",
  background: "#F3F6F8",
  border: "#DCE4E9",
  muted: "#607D8B",
  text: "#1F2937",
};

function buildChartData(records) {
  const map = {};
  records.forEach((r) => {
    if (!map[r.course_code]) {
      map[r.course_code] = { course_code: r.course_code, present: 0, absent: 0, late: 0, excused: 0 };
    }
    const key = r.status.toLowerCase();
    if (map[r.course_code][key] !== undefined) {
      map[r.course_code][key] += 1;
    }
  });
  return Object.values(map);
}

export default function StudentPortal({ studentId, onLogout }) {
  const [student, setStudent] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [risk, setRisk] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!studentId) return;

    Promise.all([
      api.get(`/students/${studentId}`),
      api.get(`/attendance/${studentId}`).catch(() => ({ data: [] })),
      api.get(`/early-warning/${studentId}`).catch(() => ({ data: null })),
    ])
      .then(([s, a, r]) => {
        setStudent(s.data);
        setAttendance(a.data);
        setRisk(r.data);
      })
      .catch(() => setError("Failed to load student data."));
  }, [studentId]);

  return (
    <div style={{ minHeight: "100vh", background: COLORS.background, fontFamily: "system-ui, sans-serif" }}>
      {/* Top navbar */}
      <header
        style={{
          background: COLORS.primary,
          color: "#FFFFFF",
          padding: "14px 28px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <img src={logo} alt="Sadat Academy" style={{ height: 36, objectFit: "contain" }} />
          <span style={{ fontWeight: 600 }}>SSI — Student Portal</span>
        </div>
        {onLogout && (
          <button
            onClick={onLogout}
            style={{
              background: "transparent",
              color: "#FFFFFF",
              border: "1px solid rgba(255,255,255,0.4)",
              padding: "6px 14px",
              borderRadius: 6,
              cursor: "pointer",
              fontSize: 13,
            }}
          >
            Logout
          </button>
        )}
      </header>

      <main style={{ padding: 28, maxWidth: 1100, margin: "0 auto" }}>
        {error && (
          <div
            style={{
              background: "#FDECEA",
              color: "#C0392B",
              border: "1px solid #F5C6C0",
              padding: 12,
              borderRadius: 8,
              marginBottom: 20,
            }}
          >
            {error}
          </div>
        )}

        {!student && !error && <p style={{ color: COLORS.muted }}>Loading…</p>}

        {student && (
          <>
            {/* Smart ID */}
            <SmartIDCard student={student} />

            {/* Risk summary */}
            {risk && (
              <div
                style={{
                  marginTop: 20,
                  background: "#FFFFFF",
                  border: `1px solid ${COLORS.border}`,
                  borderRadius: 12,
                  padding: 20,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  flexWrap: "wrap",
                  gap: 12,
                }}
              >
                <div>
                  <div style={{ fontSize: 12, color: COLORS.muted, textTransform: "uppercase" }}>
                    Academic Risk Status
                  </div>
                  <div style={{ fontSize: 18, fontWeight: 600, color: COLORS.text, marginTop: 4 }}>
                    {risk.risk_level} Risk — {risk.risk_score}%
                  </div>
                </div>
                <RiskBadge level={risk.risk_level} score={risk.risk_score} />
              </div>
            )}

            {/* Academic summary */}
            <div
              style={{
                marginTop: 20,
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                gap: 16,
              }}
            >
              {[
                { label: "GPA", value: Number(student.gpa).toFixed(2) },
                { label: "Attendance", value: `${Number(student.attendance_rate).toFixed(1)}%` },
                { label: "Credits Completed", value: student.credits_completed },
                { label: "Failed Courses", value: student.failed_courses_count },
                { label: "Current Semester", value: student.current_semester },
              ].map((item) => (
                <div
                  key={item.label}
                  style={{
                    background: "#FFFFFF",
                    border: `1px solid ${COLORS.border}`,
                    borderRadius: 12,
                    padding: 16,
                  }}
                >
                  <div style={{ fontSize: 12, color: COLORS.muted, textTransform: "uppercase" }}>
                    {item.label}
                  </div>
                  <div style={{ fontSize: 22, fontWeight: 700, color: COLORS.primary, marginTop: 6 }}>
                    {item.value}
                  </div>
                </div>
              ))}
            </div>

            {/* Attendance chart */}
            <div style={{ marginTop: 24 }}>
              <AttendanceChart data={buildChartData(attendance)} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
