import sqlite3
import pandas as pd

def main(date, start, end):
    # Path to the CSV file
    csv_file_path = 'customer_data_final.csv'

    # Read the CSV file using Pandas
    df = pd.read_csv(csv_file_path)

    # Connect to SQLite database (file-based for persistence)
    conn = sqlite3.connect('customer_data.db')
    cursor = conn.cursor()

    # Create table in SQLite database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_data (
            ID INTEGER PRIMARY KEY,
            Date TEXT,
            Time TEXT,
            Number_of_Customers INTEGER,
            Staff_Needed INTEGER
        );
    ''')

    # Insert data from CSV into the SQLite table
    df.to_sql('customer_data', conn, if_exists='replace', index=False)
    staff = 0
    startTime = int(start[:2])
    endTime = int(end[:2])
    cursor.execute("SELECT * FROM customer_data")
    data = cursor.fetchall()
    for row in data:
        if(date==row[0]):
            row_hour = int(row[1][:2])
            # Check if the hour is within the start and end time range
            if startTime <= row_hour <= endTime:
                staff += int(row[3])
    conn.close()
    return staff

# if __name__ == "__main__":
#     print(main("2022-04-16", "13:00", "15:00"))
