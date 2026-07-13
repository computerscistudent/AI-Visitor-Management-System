import csv
import os
from datetime import datetime
from app.config import ATTENDANCE_FILE

def initialize_attendance_file():
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE , 'w',newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time"])


def already_marked_today(name):
    """
    Returns True if attendance for this person
    has already been marked today.
    """

    initialize_attendance_file()

    today = datetime.now().strftime("%Y-%m-%d")

    with open(ATTENDANCE_FILE , 'r',newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (row['Name']==name and row['Date']==today) :
                return True
    return False

def mark_attendence(name):
    """
    Marks attendance if not already marked today.
    """

    initialize_attendance_file()

    if already_marked_today(name):
        print(f"{name} already marked today.")
        return False
    
    now = datetime.now()

    with open(ATTENDANCE_FILE , 'a',newline="") as file:
        writer = csv.writer(file)

        writer.writerow([name,now.strftime("%Y-%m-%d"),now.strftime("%H-%M-%S")])
    
    print(f"Attendence Marked for {name}")

    return True

def get_attendence():

    initialize_attendance_file()

    records = []

    with open(ATTENDANCE_FILE,'r',newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)
    
    return records