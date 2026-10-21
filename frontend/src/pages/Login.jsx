import { useState } from "react";
import api from "../services/api";
import logo from "../assets/logo.png";

const COLORS = {
  primary: "#173142",
  background: "#F3F6F8",
  border: "#DCE4E9",
  muted: "#607D8B",
  text: "#1F2937",
};

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await api.post("/auth/login", { username, password });
      const { access_token, role, student_id } = res.data;

      localStorage.setItem("token", access_token);
      localStorage.setItem("role", role);
      if (student_id) localStorage.setItem("student_id", student_id);

      onLogin({ role, studentId: student_id });
    } catch (err) {
      setError(
        err?.response?.data?.detail || "Login failed. Please check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: COLORS.background,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "system-ui, sans-serif",
        padding: 20,
      }}
    >
      <div
        style={{
          background: "#FFFFFF",
          border: `1px solid ${COLORS.border}`,
          borderRadius: 16,
          padding: 40,
          width: "100%",
          maxWidth: 400,
          boxShadow: "0 4px 24px rgba(23, 49, 66, 0.08)",
        }}
      >
        {/* Logo + title */}
        <div style={{ textAlign: "center", marginBottom: 28 }}>
          <img
            src={logo}
            alt="Sadat Academy"
            style={{ height: 64, objectFit: "contain", marginBottom: 12 }}
          />
          <h1 style={{ margin: 0, fontSize: 20, color: COLORS.text }}>
            Smart Student Integrated
          </h1>
          <p style={{ margin: "6px 0 0", fontSize: 13, color: COLORS.muted }}>
            Sadat Academy for Management Sciences
          </p>
        </div>

        {error && (
          <div
            style={{
              background: "#FDECEA",
              color: "#C0392B",
              border: "1px solid #F5C6C0",
              padding: 10,
              borderRadius: 8,
              fontSize: 13,
              marginBottom: 16,
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <label style={{ display: "block", fontSize: 13, color: COLORS.text, marginBottom: 6 }}>
            Username
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "10px 12px",
              border: `1px solid ${COLORS.border}`,
              borderRadius: 8,
              fontSize: 14,
              color: COLORS.text,
              marginBottom: 16,
              outline: "none",
              boxSizing: "border-box",
            }}
          />

          <label style={{ display: "block", fontSize: 13, color: COLORS.text, marginBottom: 6 }}>
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "10px 12px",
              border: `1px solid ${COLORS.border}`,
              borderRadius: 8,
              fontSize: 14,
              color: COLORS.text,
              marginBottom: 24,
              outline: "none",
              boxSizing: "border-box",
            }}
          />

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              background: COLORS.primary,
              color: "#FFFFFF",
              border: "none",
              padding: "12px",
              borderRadius: 8,
              fontSize: 14,
              fontWeight: 600,
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
              transition: "opacity 0.15s",
            }}
          >
            {loading ? "Signing in…" : "Sign In"}
          </button>
        </form>

        <p style={{ fontSize: 11, color: COLORS.muted, textAlign: "center", marginTop: 20, lineHeight: 1.6 }}>
          Demo accounts:<br />
          student / student123 &nbsp;·&nbsp; advisor / advisor123 &nbsp;·&nbsp; admin / admin123
        </p>
      </div>
    </div>
  );
}
