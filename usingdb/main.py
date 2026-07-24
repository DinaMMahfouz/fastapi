import sqlite3

conn= sqlite3.connect('school_database.db')

cursor=conn.cursor()


cursor.execute('''
               CREATE TABLE IF NOT EXISTS students( id INTEGER PRIMARY KEY, name TEXT, age INTEGER, grade INTEGER)
               ''')

# cursor.execute('''
#                INSERT INTO students(name, age, grade) VALUES ("Dina", 28, 5)
#                ''')
conn.commit()

all_students = cursor.execute('''
               SELECT * FROM students
               ''').fetchall()

first_grade_students= cursor.execute('''
               SELECT * FROM students WHERE grade = 1
               ''').fetchall()

cursor.execute('''
               UPDATE students SET grade = 3 WHERE name = "Dina"
               ''')
conn.commit()

print(all_students)

cursor.execute('''
               DELETE FROM students WHERE name = "Dina"
               ''')
conn.commit()

conn.close()