-- init.sql

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    cookie VARCHAR(255) NOT NULL
);

-- Messages table
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,  -- Foreign key to users table
    message_content TEXT NOT NULL,  -- The message text
    likes INTEGER DEFAULT 0,  -- Likes counter, starting at 0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp for when the message was created
);
