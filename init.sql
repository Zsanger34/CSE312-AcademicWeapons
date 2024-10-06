-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL, -- Username column
    password VARCHAR(255) NOT NULL, -- Password column
    cookie TEXT                     -- Cookie column
);


--Test to see if it worked
INSERT INTO users (username, password)
VALUES ('TestUser1', 'my_password123!');
--DELETE THIS TEST BEFORE SUBMITTING TO AUTOLAB

--Test to see if it worked
INSERT INTO users (username, password)
VALUES ('TestUser2', 'my_password123456789!');
--DELETE THIS TEST BEFORE SUBMITTING TO AUTOLAB

--Test to see if another table is added
CREATE TABLE IF NOT EXISTS Test (
    id SERIAL PRIMARY KEY,
    Testing VARCHAR(100) NOT NULL,
    Testcolumn VARCHAR(255) NOT NULL,
    cookie TEXT
);
