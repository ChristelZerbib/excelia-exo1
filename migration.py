import sqlite3

print("Creating DB")
conn = sqlite3.connect("fb.db")
print("DB Created")

conn.execute(
    "CREATE TABLE if not exists facebook (id INTEGER PRIMARY KEY AUTOINCREMENT, username char(100) NOT NULL UNIQUE, email char(100) NOT NULL UNIQUE, password char(100) NOT NULL, cookie char(128) UNIQUE)"
)

conn.execute(
    "INSERT INTO facebook (username, email, password) VALUES ('Marie', 'mariezerbib@gmail.com', 'TEST')"
)

conn.commit()
print("Table reated")
