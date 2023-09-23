from flask import Flask, render_template, request, redirect, session, jsonify
import csv
import os
import base64
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


db = mysql.connector.connect(
    host="db", 
    user="root",
    password="123",  
    database="mydatabase"  #I created a database named 'mydatabase' in MySQL 
)

# Create a table for users if it doesn't exist
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users2 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
""")
db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT,
    user_id VARCHAR(255) NOT NULL,
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    )
""")

db.commit()


# Helper function for printing logs
def print_table(title, key, value):
    print("================= ", title ," ===========================")
    print_row(key, value)

def print_row(key, value):
    print("|  ", key ,"      | ",value)
    print("|---------------------------------------------------------------")

# Helper functions for executing sql queries
def execute_select_query(query, params):
    print_table("SELECT QUERY FUNC", "param  ", params)
    print_row("query", query)
    cursor = db.cursor()
    cursor.execute(query, (params,))
    return cursor.fetchall()

def execute_insert_query(query, params):
    print_table("INSERT QUERY FUNC", "param  ", params)
    print_row("query", query)
    try:
        cursor = db.cursor()
        cursor.execute(query, (params,))
        db.commit()
    except mysql.connector.Error as err:
        print( "Error: ", err )
    


# Helper functions for user authentication
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def check_user_credentials(username, password):
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM users2 WHERE username = %s AND password = %s", (username, encode_password(password)))
    return cursor.fetchone() is not None



# ----------------------- Routes -----------------------------
@app.route('/')
def index():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        encoded_password = encode_password(password)
        
        #save the users details to the database:
        cursor = db.cursor()
        cursor.execute("INSERT INTO users2 (username, password) VALUES (%s, %s)", (username, encoded_password))
        db.commit()

        return redirect('/login')
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if check_user_credentials(username, password):
            session['username'] = username
            return redirect('/lobby')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')


@app.route('/health')
def health():
    return "OK, 200"


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

     
@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            # Check if the room already exists in the database
            select_query = "SELECT room_id FROM rooms WHERE room_name = %s"
            existing_room = execute_select_query( select_query , room_name)
            
            if existing_room:
                print("The given room name already exists")
            else:
                # Insert the new room into the rooms table
                insert_query = "INSERT INTO rooms (room_name) VALUES (%s)"
                execute_insert_query(insert_query, room_name)
                print(" ------------- SUCCESSFULLY CREATED NEW ROOM NAMED: " + room_name)

        # Retrieve the list of existing rooms from the database
        rooms = get_rooms_sql()
        new_rooms = [room['room_name'] for room in rooms]

        return render_template('lobby.html', rooms=new_rooms)
    else:
        return redirect('/login')

# Function to retrieve the list of rooms from SQL
def get_rooms_sql():
    select_query = "SELECT room_name FROM rooms"
    try:
        cursor = db.cursor(dictionary=True)  # Use dictionary cursor for easier data retrieval
        cursor.execute(select_query)
        rooms = cursor.fetchall()
        return rooms
    except mysql.connector.Error as err:
        print("Error retrieving rooms:", err)



@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        return render_template('chat.html', room=room)
    else:
        return redirect('/login')


@app.route('/api/chat/<room>', methods=['GET','POST'])
def update_chat(room):

    if request.method == 'POST':
        username = session['username']
        cursor = db.cursor()

        if request.args.get('clear'):
            delete_user_msg_sql(room, username, cursor)
        else:
            message = request.form['msg']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Insert the message into the messages table
            insert_message_sql(room, username, message, timestamp, cursor)

    # Retrieve messages from SQL Server
    messages = get_messages_sql(room)
    #db.close()
    return jsonify([session['username'], messages])









# ---------------------------------------------------------------------------------------------------------------#

# Helper functions for getting user and room ids by their name using sql queries

def get_user_id(cursor, username):
    get_user_id_query = "SELECT id FROM users2 WHERE username = %s"
    cursor.execute(get_user_id_query, (username,))
    user_id = cursor.fetchall()[0][0]
    return user_id

def get_room_id(cursor, room_name):
    get_room_id_query = "SELECT room_id FROM rooms WHERE room_name = %s"
    cursor.execute(get_room_id_query, (room_name,))
    room_id = cursor.fetchall()[0][0]
    return room_id



# Function to delete user messages in SQL
def delete_user_msg_sql(room_name, username, cursor):

    print("----------------- IN DELETE MESSAGE FUNC -----------------")
    # Get the room_id for the given room_name
    room_id = get_room_id(cursor, room_name)
    print_table("AFTER FIRST SELECT (room id)","room_id",room_id)
    print_row("cursor ", cursor)
    # Get the user_id for the given username
    user_id = get_user_id(cursor, username)
    print_table("AFTER SECOND SELECT (user id)", "user_id", user_id)
    print_row("cursor ", cursor)

    if room_id & user_id:
        delete_query = "DELETE FROM messages WHERE room_id = %s AND user_id = %s"
        try:
            cursor.execute(delete_query, (room_id, user_id))
            db.commit()
            print("----------------- SUCCESSFULLY DELETED MESSAGE FROM SQL-DB -----------------")
        except mysql.connector.Error as err:
            print("Error deleting user messages:", err)
    else:
        print("Error: Wrong username or room name")



# Function to insert a message into the messages table in SQL
def insert_message_sql(room_name, username, message, timestamp, cursor):
    
    print("----------------- IN INSERT MESSAGE FUNC -----------------")
    # Get the room_id for the given room_name
    room_id = get_room_id(cursor, room_name)
    print_table("AFTER FIRST SELECT (room id)","room_id",room_id)
    print_row("cursor ", cursor)
    # Get the user_id for the given username
    user_id = get_user_id(cursor, username)
    print_table("AFTER SECOND SELECT (user id)", "user_id", user_id)
    print_row("cursor ", cursor)


    if room_id:
        # Build the SQL query to insert a message
        insert_query = "INSERT INTO messages (room_id, user_id, message_text, timestamp) VALUES (%s, %s, %s, %s)"
        try:
            # Execute the insert query with parameters
            cursor.execute(insert_query, (room_id, user_id, message, timestamp))
            db.commit()  # Commit the changes
            print("----------------- SUCCESSFULLY INSERTED THE MESSAGE TO SQL-DB ----------------")
        except mysql.connector.Error as err:
            print("Error inserting a message:", err)
    else:
        print("Error: Wrong username or room name")






# Function to retrieve messages for the specified room from SQL
def get_messages_sql(room_name):
    print("----------------- IN GET MESSAGE FUNC -----------------")

    # Build the SQL query to retrieve messages with user names
    select_query = """
        SELECT u.username, m.message_text, m.timestamp
        FROM messages m
        INNER JOIN users2 u ON m.user_id = u.id
        WHERE m.room_id = (SELECT room_id FROM rooms WHERE room_name = %s)
        ORDER BY m.timestamp
    """
    try:
        cursor = db.cursor()  
        # Execute the select query with parameters
        cursor.execute(select_query, (room_name,))
        messages = []
        for (username, message_text, timestamp) in cursor:
            messages.append({
                "username": username,
                "message_text": message_text,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        print("----------------- SUCCESSFULLY RECEVED THE MESSAGES FROM SQL DB -----------------")
        return messages
    except mysql.connector.Error as err:
        print("Error executing SQL query:", select_query)
        print("Error message:", err)




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


