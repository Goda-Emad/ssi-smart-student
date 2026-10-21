import { useEffect, useState } from "react";
import api from "../services/api";
import logo from "../assets/logo.png";

const COLORS = {
  primary: "#173142",
  background: "#F3F6F8",
  border: "#DCE4E9",
  muted: "#607D8B",
  text: "#1F2937",
};

function StatCard({ label, value, accent = COLORS.primary }) {
  return (
    <div
      style={{
        background: "#FFFFFF",
        border: `1px solid ${COLORS.border}`,
        borderRadius: 12,
        padding: 20,
        flex: 1,
        minWidth: 180,
      }}
    >
      <div style={{ fontSize: 12, color: COLORS.muted, textTransform: "uppercase", letterSpacing: 0.5 }}>
        {label}
      </div>
      <div style={{ fontSize: 28, fontWeight: 700, color: accent, marginTop: 8 }}>
        {value}
      </div>
    </div>
  );
}

export default function AdminDashboard({ onLogout }) {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/dashboard/summary")
      .then((res) => setSummary(res.data))
      .catch(() => setError("Failed to load dashboard summary."));
  }, []);

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
          <span style={{ fontWeight: 600 }}>SSI — Admin Dashboard</span>
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

      <main style={{ padding: 28, maxWidth: 1200, margin: "0 auto" }}>
        <h1 style={{ color: COLORS.text, fontSize: 22, marginBottom: 20 }}>
          System Overview
        </h1>

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

        {!summary && !error && (
          <p style={{ color: COLORS.muted }}>Loading…</p>
        )}

        {summary && (
          <>
            <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 28 }}>
              <StatCard label="Total Students" value={summary.total_students} />
              <StatCard
                label="At-Risk Students"
                value={summary.at_risk_students}
                accent="#C0392B"
              />
              <StatCard label="At-Risk %" value={`${summary.at_risk_percentage}%`} accent="#C0392B" />
              <StatCard label="Average GPA" value={summary.average_gpa} />
              <StatCard label="Average Attendance" value={`${summary.average_attendance}%`} />
            </div>

            <div
              style={{
                background: "#FFFFFF",
                border: `1px solid ${COLORS.border}`,
                borderRadius: 12,
                padding: 20,
              }}
            >
              <h3 style={{ margin: "0 0 16px", color: COLORS.text, fontSize: 16 }}>
                Students by Faculty
              </h3>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
                <thead>
                  <tr style={{ background: COLORS.background }}>
                    <th style={{ textAlign: "left", padding: "10px 12px", color: COLORS.muted, fontSize: 12 }}>
                      Faculty
                    </th>
                    <th style={{ textAlign: "left", padding: "10px 12px", color: COLORS.muted, fontSize: 12 }}>
                      Students
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {summary.students_by_faculty.map((row) => (
                    <tr key={row.faculty} style={{ borderBottom: `1px solid ${COLORS.border}` }}>
                      <td style={{ padding: "10px 12px", color: COLORS.text }}>{row.faculty}</td>
                      <td style={{ padding: "10px 12px", color: COLORS.text }}>{row.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
