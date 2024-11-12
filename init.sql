CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    profile_id VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    cookie VARCHAR(255) NOT NULL
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,  
    message_content TEXT NOT NULL,  
    likes INTEGER DEFAULT 0, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_like_list INTEGER[]
);



CREATE TABLE profilePages (
    profile_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,  
    bio VARCHAR(255) UNIQUE NOT NULL,  
    followers VARCHAR[], 
    following VARCHAR[],
    MyPosts INTEGER[]
);

