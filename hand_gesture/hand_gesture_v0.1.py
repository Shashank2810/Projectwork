#pip install opencv-python
#pip install mediapipe
#pip install keyboard
#pip install pycaw





import cv2
import mediapipe as mp
import keyboard

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize volume control variables
thumbs_up_detected = False
thumbs_down_detected = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image with Mediapipe Hands
    results = hands.process(frame_rgb)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Calculate thumb tip coordinates
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])

            # Detect thumbs-up or thumbs-down gesture based on thumb tip position
            if thumb_x < frame.shape[1] // 2:
                thumbs_down_detected = True
                thumbs_up_detected = False
            else:
                thumbs_up_detected = True
                thumbs_down_detected = False

        # Handle volume control based on the detected gesture
        if thumbs_up_detected:
            keyboard.press('volume up')  # Press volume up key
        elif thumbs_down_detected:
            keyboard.press('volume down')  # Press volume down key

    else:
        thumbs_up_detected = False
        thumbs_down_detected = False
        keyboard.release('volume up')  # Release volume up key
        keyboard.release('volume down')  # Release volume down key

    # Display the frame
    cv2.imshow('Hand Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
