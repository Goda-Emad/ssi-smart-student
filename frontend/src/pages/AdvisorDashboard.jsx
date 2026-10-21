import { useEffect, useState } from "react";
import api from "../services/api";
import logo from "../assets/logo.png";
import StudentTable from "../components/StudentTable";

const COLORS = {
  primary: "#173142",
  background: "#F3F6F8",
  border: "#DCE4E9",
  muted: "#607D8B",
  text: "#1F2937",
};

export default function AdvisorDashboard({ onLogout }) {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    api
      .get("/early-warning/at-risk")
      .then((res) => setStudents(res.data))
      .catch(() => setError("Failed to load at-risk students."))
      .finally(() => setLoading(false));
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
          <span style={{ fontWeight: 600 }}>SSI — Advisor Dashboard</span>
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
        <div style={{ marginBottom: 20 }}>
          <h1 style={{ color: COLORS.text, fontSize: 22, margin: 0 }}>
            At-Risk Students
          </h1>
          <p style={{ color: COLORS.muted, fontSize: 14, marginTop: 6 }}>
            Students flagged by the AI Early Warning system, sorted by risk score.
          </p>
        </div>

        {loading && <p style={{ color: COLORS.muted }}>Loading…</p>}
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

        {!loading && !error && (
          <StudentTable students={students} onSelect={(s) => setSelected(s)} />
        )}

        {/* Selected student panel */}
        {selected && (
          <div
            style={{
              marginTop: 20,
              background: "#FFFFFF",
              border: `1px solid ${COLORS.border}`,
              borderRadius: 12,
              padding: 20,
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <h3 style={{ margin: 0, color: COLORS.text, fontSize: 16 }}>
                {selected.full_name} ({selected.student_id})
              </h3>
              <button
                onClick={() => setSelected(null)}
                style={{
                  background: "transparent",
                  border: `1px solid ${COLORS.border}`,
                  color: COLORS.muted,
                  padding: "4px 10px",
                  borderRadius: 6,
                  cursor: "pointer",
                  fontSize: 12,
                }}
              >
                Close
              </button>
            </div>

            <div style={{ display: "flex", gap: 24, marginTop: 16, flexWrap: "wrap", fontSize: 14 }}>
              <div>
                <div style={{ color: COLORS.muted, fontSize: 12 }}>Faculty</div>
                <div style={{ color: COLORS.text }}>{selected.faculty}</div>
              </div>
              <div>
                <div style={{ color: COLORS.muted, fontSize: 12 }}>GPA</div>
                <div style={{ color: COLORS.text }}>{Number(selected.gpa).toFixed(2)}</div>
              </div>
              <div>
                <div style={{ color: COLORS.muted, fontSize: 12 }}>Attendance</div>
                <div style={{ color: COLORS.text }}>{Number(selected.attendance_rate).toFixed(1)}%</div>
              </div>
              <div>
                <div style={{ color: COLORS.muted, fontSize: 12 }}>Risk Score</div>
                <div style={{ color: "#C0392B", fontWeight: 600 }}>{selected.risk_score}%</div>
              </div>
              <div>
                <div style={{ color: COLORS.muted, fontSize: 12 }}>Risk Level</div>
                <div style={{ color: COLORS.text }}>{selected.risk_level}</div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
