import sqlite3

"""
    This file creates a database and two
    tables called users and tweets, with its fields. only
    you need to run it once.
"""

#If the database is not created, but if it exists, it makes the connection.
Connection = sqlite3.connect("./database.db") 

cursor = Connection.cursor()

#Try to create the table, only fails if the table already exists.
try:
    cursor.execute("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(30) NOT NULL UNIQUE,
            email VARCHAR(30) NOT NULL UNIQUE,
            user_name VARCHAR(20) NOT NULL UNIQUE,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            birth_date timestamp,
            password VARCHAR(64) NOT NULL
        )
    """)

except Exception as e:
    print(f"{type(e).__name__}: {e}")
    

#close the connection.
Connection.close()