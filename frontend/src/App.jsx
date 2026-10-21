import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";

import Login from "./pages/Login";
import StudentPortal from "./pages/StudentPortal";
import AdvisorDashboard from "./pages/AdvisorDashboard";
import AdminDashboard from "./pages/AdminDashboard";

function AppRoutes() {
  const navigate = useNavigate();
  const [auth, setAuth] = useState(() => ({
    role: localStorage.getItem("role"),
    studentId: localStorage.getItem("student_id"),
  }));

  // Sync auth state from localStorage on mount
  useEffect(() => {
    setAuth({
      role: localStorage.getItem("role"),
      studentId: localStorage.getItem("student_id"),
    });
  }, []);

  const handleLogin = ({ role, studentId }) => {
    setAuth({ role, studentId });
    if (role === "student") navigate("/student");
    else if (role === "advisor") navigate("/advisor");
    else if (role === "admin") navigate("/admin");
    else navigate("/login");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("student_id");
    setAuth({ role: null, studentId: null });
    navigate("/login");
  };

  return (
    <Routes>
      <Route
        path="/login"
        element={
          auth.role ? (
            <Navigate
              to={auth.role === "student" ? "/student" : `/${auth.role}`}
              replace
            />
          ) : (
            <Login onLogin={handleLogin} />
          )
        }
      />

      <Route
        path="/student"
        element={
          auth.role === "student" ? (
            <StudentPortal studentId={auth.studentId} onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      <Route
        path="/advisor"
        element={
          auth.role === "advisor" ? (
            <AdvisorDashboard onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      <Route
        path="/admin"
        element={
          auth.role === "admin" ? (
            <AdminDashboard onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      <Route
        path="*"
        element={
          <Navigate
            to={auth.role ? (auth.role === "student" ? "/student" : `/${auth.role}`) : "/login"}
            replace
          />
        }
      />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
