CREATE TABLE users4 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('user1', 'password1');
INSERT INTO users (username, password) VALUES ('user2', 'password2');


-- # Create a table for users if it doesn't exist
-- db = mysql.connector.connect(
--     host="localhost", 
--     user="root",
--     password="123",  
--     database="mydatabase"  #I created a database named 'mydatabase' in MySQL 
-- )
-- cursor = db.cursor()

-- cursor.execute("""
--     CREATE TABLE IF NOT EXISTS users2 (
--         id INT AUTO_INCREMENT PRIMARY KEY,
--         username VARCHAR(255) NOT NULL,
--         password VARCHAR(255) NOT NULL
--     )
-- """)
-- db.commit()

-- cursor.execute("""
--     CREATE TABLE IF NOT EXISTS messages (
--     message_id INT AUTO_INCREMENT PRIMARY KEY,
--     room_id INT,
--     user_id VARCHAR(255) NOT NULL,
--     message_text TEXT NOT NULL,
--     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (room_id) REFERENCES rooms(room_id)
--     )
-- """)

-- db.commit()
-- cursor.execute("""
--     CREATE TABLE IF NOT EXISTS rooms (
--     room_id INT AUTO_INCREMENT PRIMARY KEY,
--     room_name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--     )
-- """)
-- db.commit()