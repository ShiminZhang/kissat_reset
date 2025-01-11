import sqlite3

conn = sqlite3.connect('meta.db')
cursor = conn.cursor()
target = "7cbc3ce2052ba7c5b501f75af58ab3c4"
cursor.execute(f"SELECT hash, family FROM features WHERE hash = '{target}'")
result = cursor.fetchall()

print(result)

conn.close()
