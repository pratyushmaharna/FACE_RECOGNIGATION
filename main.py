import cv2
import face_recognition
import os
import sqlite3
from datetime import datetime

# Load known faces
known_encodings = []
known_names = []

for file in os.listdir("known_faces"):
    if file.endswith(".jpg") or file.endswith(".png"):
        try:
            img = face_recognition.load_image_file(f"known_faces/{file}")
            encodings = face_recognition.face_encodings(img)
            if len(encodings) > 0:  # only add if a face is found
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(file)[0])
                print(f"Loaded {file}")
            else:
                print(f"No face found in {file}, skipping.")
        except Exception as e:
            print(f"Error loading {file}: {e}")

def mark_attendance(name):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE name=?", (name,))
    result = cursor.fetchone()
    if result:
        student_id = result[0]
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        cursor.execute("INSERT INTO attendance (student_id, date, time, status) VALUES (?, ?, ?, ?)",
                       (student_id, date, time, "Present"))
        conn.commit()
    conn.close()

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, locations)

    for encoding, loc in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_names[index]
            mark_attendance(name)

        top, right, bottom, left = loc
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()