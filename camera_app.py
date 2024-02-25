from roboflow import Roboflow
import supervision as sv
import cv2
import time
import threading
from functools import partial
import sqlite3

def count_people_in_image(image_path):
    rf = Roboflow(api_key="VoxPG3IJf5NMAzTmMU3z")
    project = rf.workspace().project("crowd_count_v2")
    model = project.version(2).model

    result = model.predict(image_path, confidence=12, overlap=70).json()
    detections = sv.Detections.from_roboflow(result)
    return len(detections)

def update_people_count_callback(people_count):
    # Update the people count in the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Assuming you have a way to identify the correct restaurant entry to update
    c.execute("UPDATE restaurants SET people_count = ? WHERE name = ?", (people_count, "ExampleRestaurant"))
    conn.commit()
    print(f"Updated count to {people_count} in the database.")  # Debug print
    conn.close()

def capture_live_frames(update_people_count_callback):
    cap = cv2.VideoCapture(0)  # Use the appropriate device index or video file
    start_time = time.time()
    print("Starting camera capture...")
    while True:
        # print("Capturing frame...")
        ret, frame = cap.read()
        # if not ret:
        #     print("Failed to capture frame.")
        #     break

        # # Show the frame for debugging purposes
        # cv2.imshow('Frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     print("Quitting...")
        #     break

        # Check if 30 seconds have passed
        if time.time() - start_time >= 15:
            # Reset the timer
            print("10 seconds passed, processing frame...")
            start_time = time.time()

            # Save the current frame as an image
            frame_path = 'current_frame.jpg'
            cv2.imwrite(frame_path, frame)

            # Pass the image to the ML function and get the number of people detected
            people_count = count_people_in_image(frame_path)

            # Call the callback function with the new people count
            update_people_count_callback(people_count)

            print(f"People Count: {people_count}")

    cap.release()
    cv2.destroyAllWindows()
