from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from camera_app import capture_live_frames
import threading
from camera_app import update_people_count_callback
import pandas as pd
from deepface import DeepFace
import cv2
import time
#from face_rec import capture_live_faces
# from staffing import main


app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants (name TEXT UNIQUE, password TEXT, people_count INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Function to update the people count
def update_people_count(name, people_count):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE restaurants SET people_count = ? WHERE name = ?", (people_count, name))
    conn.commit()
    conn.close()

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     message = ''
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']
#         conn = sqlite3.connect('database.db')
#         c = conn.cursor()
#         # Check if the restaurant already exists
#         c.execute("SELECT * FROM restaurants WHERE name = ?", (name,))
#         entry = c.fetchone()
#         if entry:
#             # Update existing entry with new password (optional)
#             c.execute("UPDATE restaurants SET password = ? WHERE name = ?", (password, name))
#         else:
#             # Insert new entry if restaurant does not exist
#             c.execute("INSERT INTO restaurants (name, password, people_count) VALUES (?, ?, ?)", (name, password, 0))
#         conn.commit()
#         conn.close()

#         # Start the camera script in a separate thread
#         thread = threading.Thread(target=capture_live_frames, args=(lambda: update_people_count(name, _),))
#         thread.start()

#         message = 'Login Successful'
#     return render_template('login.html', message=message)
    

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     message = ''
#     if request.method == 'POST':
#         name = request.form['name']
#         password = request.form['password']

#         # Check credentials (for demonstration, using hardcoded values)
#         if name == "ExampleRestaurant" and password == "examplePassword":
#             # Start the camera script in a separate thread
#             # thread = threading.Thread(target=capture_live_frames)
#             # thread.start()
#             thread = threading.Thread(target=capture_live_frames, args=(update_people_count_callback,))
#             thread.start()

#             # Redirect to the counter page
#             return redirect(url_for('counter'))
#         else:
#             message = 'Invalid credentials'
#     return render_template('login.html', message=message)
    

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if name == "ExampleRestaurant" and password == "examplePassword":
            # Start the camera script in a separate thread
            thread = threading.Thread(target=capture_live_frames, args=(update_people_count_callback,))
            thread.daemon = True  # Ensure thread doesn't prevent app from exiting
            thread.start()

            # Redirect to menu input page
            # return redirect(url_for('choose_action'))
            return render_template('choose_action.html')
        else:
            message = 'Invalid credentials'
    return render_template('login.html', message=message)


@app.route('/staffing', methods=['GET', 'POST'])
def staffing():
    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        print(date,start_time,end_time)
        staff_needed = dynamicStaffing(date, start_time, end_time)
        return render_template('staffing_result.html', staff_needed=staff_needed)
    return render_template('staffing.html')


@app.route('/staff-rec')
def staff_rec():
    message =  capture_live_faces()
    return render_template('staff_rec.html', message = message)

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
    result = DeepFace.verify(img1_path = "Photos/13.png",img2_path=frame_path)
    return(result['verified'])

def dynamicStaffing(date, start, end):
    conn = sqlite3.connect('customer_data.db')
    cursor = conn.cursor()
    staff = 0
    startTime = int(start[:2])
    endTime = int(end[:2])
    cursor.execute("SELECT * FROM customer_data WHERE Date = ?", (date,))
    data = cursor.fetchall()
    for row in data:
        row_hour = int(row[1][:2])
        if startTime <= row_hour <= endTime:
            staff += int(row[3])
    conn.close()
    return staff

# @app.route('/counter')
# def counter():
#     print("Check 1")
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     print("Check 2")
#     # Assuming there's only one entry for now, but you should implement a proper check based on your app's logic
#     c.execute("SELECT people_count FROM restaurants ORDER BY ROWID ASC LIMIT 1")
#     row = c.fetchone()
#     print("Check 3")
#     conn.close()
#     print("Check 4")
#     if row:  # Check if row is not None
#         print("Check 5")
#         people_count = row[0]
#     else:
#         print("Check 6")
#         people_count = 0  # Default to 0 if no entry is found

#     print(f"TESTER {people_count} TESTER.")

#     return render_template('counter.html', people_count=people_count)

@app.route('/menu_input', methods=['GET', 'POST'])
def menu_input():
    if request.method == 'POST':
        item_name = request.form['item_name']
        base_price = request.form['base_price']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO menu_items (item_name, base_price) VALUES (?, ?)", (item_name, base_price))
        conn.commit()
        conn.close()

        return redirect(url_for('menu_display'))  # Redirect to the menu display page after item insertion

    return render_template('menu_input.html')

@app.route('/menu_display')
def menu_display():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get the current people count
    c.execute("SELECT people_count FROM restaurants ORDER BY ROWID ASC LIMIT 1")
    row = c.fetchone()
    people_count = row[0] if row else 0

    # Get all menu items
    c.execute("SELECT item_name, base_price FROM menu_items")
    # menu_items = [{'item_name': row[0], 'dynamic_price': row[1] * 1.05 * people_count} for row in c.fetchall()]
    menu_items = [
    {
        'item_name': row[0], 
        'dynamic_price': row[1] * 0.75 if people_count >= 9 else (row[1] * 0.9 if people_count >= 6 else row[1])
    } 
    for row in c.fetchall()
]

    conn.close()

    # people_count = get_people_count()  # This should be your actual function or method to get the count
    # menu_items = get_menu_items()  # This should be your actual function or method to retrieve menu items

    return render_template('menu_display.html', menu_items=menu_items, people_count=people_count)
    # return render_template('menu_display.html', menu_items=menu_items)




# @app.route('/menu_input', methods=['GET', 'POST'])
# def menu_input():
#     if request.method == 'POST':
#         item_name = request.form['item_name']
#         base_price = request.form['base_price']

#         conn = sqlite3.connect('database.db')
#         c = conn.cursor()
#         c.execute("INSERT INTO menu_items (item_name, base_price) VALUES (?, ?)", (item_name, base_price))
#         conn.commit()
#         conn.close()

#         return redirect(url_for('menu_display'))  # Redirect to the menu display page after item insertion

#     return render_template('menu_input.html')


# @app.route('/add_menu_item', methods=['GET', 'POST'])
# def add_menu_item():
#     if request.method == 'POST':
#         item_name = request.form['item_name']
#         base_price = request.form['base_price']
        
#         # Insert into database
#         conn = sqlite3.connect('database.db')
#         c = conn.cursor()
#         c.execute("INSERT INTO menu_items (item_name, base_price) VALUES (?, ?)", (item_name, base_price))
#         conn.commit()
#         conn.close()

#         return redirect(url_for('view_menu'))

#     return render_template('add_menu_item.html')


if __name__ == '__main__':
    app.run(port=5003, debug=True)
