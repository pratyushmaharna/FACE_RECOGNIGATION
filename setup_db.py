import sqlite3

# Create database and tables
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    time TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)
""")

conn.commit()
conn.close()

# Function to add students safely
def add_student(name, roll_number):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, roll_number) VALUES (?, ?)", (name, roll_number))
        conn.commit()
        print(f"Student {name} added successfully!")
    except sqlite3.IntegrityError:
        print(f"Roll number {roll_number} already exists, skipping.")
    conn.close()

# Add sample students
add_student("Pratyush", "CS101")
add_student("Ananya", "CS102")

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()