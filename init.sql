-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL, -- Username column
    password VARCHAR(255) NOT NULL, -- Password column
    cookie TEXT                     -- Cookie column
);