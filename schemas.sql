
-- CREATE DATABASE student_management_db;

-- Connect to the database before running the rest:
-- \c student_management_db

-- 1. Create the departments table
-- This will hold all academic departments (e.g., CSE, ECE, MBA)
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,                    -- Auto-incrementing primary key
    name VARCHAR(100) NOT NULL UNIQUE,        -- Department name (must be unique)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- When department was added
);

-- 2. Create the students table
-- This holds student records with foreign key to departments
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,                    -- Auto-incrementing primary key
    name VARCHAR(100) NOT NULL,               -- Student's full name
    email VARCHAR(150) NOT NULL UNIQUE,       -- Unique email (prevents duplicates)
    phone VARCHAR(15) UNIQUE,                 -- Optional: unique phone number
    department_id INTEGER,                    -- Foreign key to departments table
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When student was added
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When student record was last updated

    -- Foreign key constraint (handles deletion safely)
    CONSTRAINT fk_students_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL  -- If department deleted, student's dept becomes NULL (not deleted)
);

-- 3. Create indexes for optimized search performance (this is your 60% speed boost!)
-- Index on student name for fast partial matches (LIKE queries)
CREATE INDEX IF NOT EXISTS idx_students_name 
ON students (name);

-- Index on email for fast unique lookups
CREATE INDEX IF NOT EXISTS idx_students_email 
ON students (email);

-- Index on department_id for fast filtering by department
CREATE INDEX IF NOT EXISTS idx_students_dept 
ON students (department_id);

-- 4. Optional: Index on email for case-insensitive searches (if needed)
-- CREATE INDEX IF NOT EXISTS idx_students_email_lower 
-- ON students (LOWER(email));

-- 5. Optional: Index for faster sorting by creation date
CREATE INDEX IF NOT EXISTS idx_students_created_at 
ON students (created_at);

-- 6. Insert default departments (optional - for testing)
-- Uncomment below if you want sample data:
/*
INSERT INTO departments (name) VALUES 
    ('Computer Science & Engineering'),
    ('Electronics & Communication'),
    ('Mechanical Engineering'),
    ('Electrical Engineering'),
    ('Civil Engineering'),
    ('MBA'),
    ('MCA');
*/
