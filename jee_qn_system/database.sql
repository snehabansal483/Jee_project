-- Create the database
CREATE DATABASE IF NOT EXISTS jee_db;
USE jee_db;

-- Table for Users (Admin and Students)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL, -- Storing plain text as requested for simplicity
    role ENUM('admin', 'student') NOT NULL
);

-- Table for Questions
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(50) NOT NULL,
    chapter VARCHAR(100) NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(200) NOT NULL,
    option_b VARCHAR(200) NOT NULL,
    option_c VARCHAR(200) NOT NULL,
    option_d VARCHAR(200) NOT NULL,
    correct_answer CHAR(1) NOT NULL, -- Stores 'A', 'B', 'C', or 'D'
    difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL
);

-- Insert Dummy Data for Users
-- Admin: username 'admin', password 'admin123'
-- Student: username 'student', password 'student123'
INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'admin'),
('student', 'student123', 'student');

-- Insert Dummy Data for Questions
INSERT INTO questions (subject, chapter, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty) VALUES 
('Physics', 'Kinematics', 'A car travels 100km in 2 hours. What is its speed?', '40 km/h', '50 km/h', '60 km/h', '100 km/h', 'B', 'Easy'),
('Mathematics', 'Calculus', 'What is the derivative of x^2?', 'x', '2x', 'x^2', '2', 'B', 'Easy'),
('Chemistry', 'Atomic Structure', 'Who discovered the electron?', 'Rutherford', 'Chadwick', 'Thomson', 'Bohr', 'C', 'Medium');
