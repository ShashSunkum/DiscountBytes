from deepface import DeepFace
import cv2
import time

def capture_live_faces():
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
        if time.time() - start_time >= 7:
            # Reset the timer
            print("15 seconds passed, processing frame...")
            start_time = time.time()

            # Save the current frame as an image
            frame_path = 'current_frame.jpg'
            cv2.imwrite(frame_path, frame)

            # Pass the image to the ML function and get the number of people detected
            clocked_in = recognize_people(frame_path)

            if(clocked_in):
                return("This is Shashwath Sunkum........>>>>>Clocked IN")
            else:
                return("Not recognized")
            # # Call the callback function with the new people count
            # update_people_count_callback(people_count)

            # print(f"People Count: {people_count}")

    cap.release()
    cv2.destroyAllWindows()

def recognize_people(frame_path):
    result = DeepFace.verify(img1_path = "Photos/12.png",img2_path=frame_path)
    return(result['verified'])
     
print(capture_live_faces())
  


