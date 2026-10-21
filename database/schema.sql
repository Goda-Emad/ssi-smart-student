-- ============================================================
-- SSI — Database Schema (SQLite)
-- ============================================================

CREATE TABLE IF NOT EXISTS students (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id            VARCHAR(20) UNIQUE NOT NULL,
    full_name             VARCHAR(150) NOT NULL,
    gender                VARCHAR(10)  NOT NULL,
    age                   INTEGER      NOT NULL,
    faculty               VARCHAR(100) NOT NULL,
    department            VARCHAR(100) NOT NULL,
    academic_year         INTEGER      NOT NULL,
    enrollment_type       VARCHAR(30)  NOT NULL,
    admission_score       FLOAT        NOT NULL,
    gpa                   FLOAT        NOT NULL DEFAULT 0.0,
    total_credits         INTEGER      NOT NULL DEFAULT 0,
    credits_completed     INTEGER      NOT NULL DEFAULT 0,
    failed_courses_count  INTEGER      NOT NULL DEFAULT 0,
    current_semester      INTEGER      NOT NULL DEFAULT 1,
    attendance_rate       FLOAT        NOT NULL DEFAULT 0.0,
    absence_days          INTEGER      NOT NULL DEFAULT 0,
    late_submissions      INTEGER      NOT NULL DEFAULT 0,
    library_visits        INTEGER      NOT NULL DEFAULT 0,
    lms_logins            INTEGER      NOT NULL DEFAULT 0,
    extracurricular       VARCHAR(5)   NOT NULL DEFAULT 'No',
    disciplinary_actions  INTEGER      NOT NULL DEFAULT 0,
    tuition_status        VARCHAR(20)  NOT NULL DEFAULT 'Paid',
    financial_aid         VARCHAR(5)   NOT NULL DEFAULT 'No',
    previous_warnings     INTEGER      NOT NULL DEFAULT 0,
    advisor_meetings      INTEGER      NOT NULL DEFAULT 0,
    stress_level          INTEGER      NOT NULL DEFAULT 0,
    part_time_job         VARCHAR(5)   NOT NULL DEFAULT 'No',
    commute_distance_km   FLOAT        NOT NULL DEFAULT 0.0,
    risk_label            INTEGER      NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS academic_records (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id            INTEGER UNIQUE NOT NULL,
    gpa                   FLOAT   NOT NULL DEFAULT 0.0,
    total_credits         INTEGER NOT NULL DEFAULT 0,
    credits_completed     INTEGER NOT NULL DEFAULT 0,
    failed_courses_count  INTEGER NOT NULL DEFAULT 0,
    current_semester      INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id         VARCHAR(20) UNIQUE NOT NULL,
    student_id        INTEGER NOT NULL,
    course_code       VARCHAR(20)  NOT NULL,
    course_name       VARCHAR(150) NOT NULL,
    semester          INTEGER      NOT NULL,
    session_date      DATE         NOT NULL,
    session_type      VARCHAR(20)  NOT NULL,
    status            VARCHAR(20)  NOT NULL,
    duration_minutes  INTEGER      NOT NULL DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS risk_scores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL,
    risk_label  INTEGER NOT NULL,
    risk_score  FLOAT   NOT NULL,
    risk_level  VARCHAR(20) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_students_student_id    ON students(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student     ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_record      ON attendance(record_id);
CREATE INDEX IF NOT EXISTS idx_risk_student           ON risk_scores(student_id);
