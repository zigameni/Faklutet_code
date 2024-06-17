-- Drop the user table if it exists (optional, use with caution)
DROP TABLE IF EXISTS user;

-- Create the user table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);

-- Delete existing data (optional, use with caution)
DELETE FROM user;

-- Insert initial users with unique emails
INSERT INTO user (username, email) VALUES ('admin', 'admin@example.com');
INSERT INTO user (username, email) VALUES ('user1', 'user1@example.com');
INSERT INTO user (username, email) VALUES ('user2', 'user2@example.com');
INSERT INTO user (username, email) VALUES ('user3', 'user3@example.com');
INSERT INTO user (username, email) VALUES ('user4', 'user4@example.com');
-- Add more users as needed