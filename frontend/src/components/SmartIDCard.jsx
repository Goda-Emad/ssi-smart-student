import { useEffect, useState } from "react";
import api from "../services/api";
import logo from "../assets/logo.png";

export default function SmartIDCard({ student }) {
  const [qrUrl, setQrUrl] = useState(null);

  useEffect(() => {
    if (!student?.student_id) return;

    let objectUrl = null;
    api
      .get(`/students/${student.student_id}/qr`, { responseType: "blob" })
      .then((res) => {
        objectUrl = URL.createObjectURL(res.data);
        setQrUrl(objectUrl);
      })
      .catch(() => setQrUrl(null));

    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [student?.student_id]);

  if (!student) return null;

  return (
    <div
      style={{
        background: "#173142",
        color: "#FFFFFF",
        borderRadius: 16,
        padding: 24,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        gap: 24,
        boxShadow: "0 4px 16px rgba(23, 49, 66, 0.15)",
        maxWidth: 520,
      }}
    >
      {/* Left: student info */}
      <div style={{ flex: 1 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
          <img
            src={logo}
            alt="Sadat Academy"
            style={{ height: 40, width: "auto", objectFit: "contain" }}
          />
          <div style={{ fontSize: 12, opacity: 0.85, lineHeight: 1.3 }}>
            Sadat Academy
            <br />
            for Management Sciences
          </div>
        </div>

        <div style={{ fontSize: 20, fontWeight: 700, marginBottom: 4 }}>
          {student.full_name}
        </div>
        <div style={{ fontSize: 13, opacity: 0.85, marginBottom: 12 }}>
          ID: {student.student_id}
        </div>

        <div style={{ fontSize: 13, opacity: 0.85, lineHeight: 1.6 }}>
          <div>{student.faculty}</div>
          <div>{student.department}</div>
          <div>Year {student.academic_year}</div>
        </div>
      </div>

      {/* Right: QR */}
      <div
        style={{
          background: "#FFFFFF",
          padding: 8,
          borderRadius: 12,
          width: 120,
          height: 120,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {qrUrl ? (
          <img src={qrUrl} alt="Student QR" style={{ width: "100%", height: "100%" }} />
        ) : (
          <span style={{ fontSize: 11, color: "#607D8B" }}>Loading QR…</span>
        )}
      </div>
    </div>
  );
}
