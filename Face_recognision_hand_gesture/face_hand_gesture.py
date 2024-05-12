# Required packages
# pip install cmake face_recognition opencv-python numpy dlib pyttsx3 requests mediapipe keyboard pycaw

import cv2
import numpy as np
import csv
from datetime import datetime
import pyttsx3
import mediapipe as mp
import keyboard
import face_recognition

def speak_text(text):
    speak = pyttsx3.init()
    speak.say(text)
    speak.runAndWait()

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load known images for face recognition
face1_image = face_recognition.load_image_file(r"faces\face1.JPG")
face1_encoding = face_recognition.face_encodings(face1_image)[0]

face2_image = face_recognition.load_image_file(r"faces\face2.JPG")
face2_encoding = face_recognition.face_encodings(face2_image)[0]

known_face_encodings = [face1_encoding, face2_encoding]
known_face_names = ["face1", "face2"]

# List of expected people
people = known_face_names.copy()

video_capture = cv2.VideoCapture(0)

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    # Resize frame to process faster
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Face recognition
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name in people:
                speak_text(f"{name} is recognized. You can now control the volume.")
                people.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name, current_time])

    # Process the image with Mediapipe Hands for hand gesture detection
    results = hands.process(rgb_small_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])

            if thumb_x < frame.shape[1] // 2:
                keyboard.press('volume down')
            else:
                keyboard.press('volume up')
    else:
        keyboard.release('volume down')
        keyboard.release('volume up')

    # Display face recognition results
    for (top, right, bottom, left), name in zip(face_locations, known_face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Show video feed
    cv2.imshow("Recognize", frame)

    # Break loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release webcam and close windows
video_capture.release()
cv2.destroyAllWindows()
f.close()
