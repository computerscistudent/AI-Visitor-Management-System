import csv
import os
from datetime import datetime
from app.config import ATTENDANCE_FILE
from app.models.models import Visitor, Attendance
from app.database import db


#*************** utility functions for DataBase based attendance marking. ************************

def already_marked_today(name):
    """
    Returns True if attendance has already been
    marked today for this visitor.
    """
    visitor = Visitor.query.filter_by(name=name).first()
    if visitor is None:
        return False
    
    today = datetime.now().date()

    attendance = Attendance.query.filter_by(visitor_id=visitor.id,date=today).first()

    return attendance is not None

def mark_attendance(name):
    """
    Marks attendance in PostgreSQL.
    """

    visitor = Visitor.query.filter_by(name=name).first()
    if visitor is None:
        print(f"{name} not found in database.")
        return False
    
    if already_marked_today(name):
        print(f"{name} already marked today.")
        return False
    
    now = datetime.now()

    attendance = Attendance(visitor_id=visitor.id,date=now.date(),time=now.time()) # type:ignore

    db.session.add(attendance)
    db.session.commit()

    print(f"Attendance marked for {name}")

    return True

def get_attendance():

    records = []

    attendence_list = (db.session.query(Attendance,Visitor).join(Visitor).order_by(Attendance.date.desc(),Attendance.time.desc()).all())

    for attendance, visitor in attendence_list:
        records.append({
            'Name':visitor.name,
            "Date": attendance.date.strftime("%Y-%m-%d"),
            "Time": attendance.time.strftime("%H:%M:%S"),
            "Photo": visitor.photo_path
        })
    return records



#*************** utility functions for csv based attendance marking. **************************
# def initialize_attendance_file():
#     if not os.path.exists(ATTENDANCE_FILE):
#         with open(ATTENDANCE_FILE , 'w',newline="") as file:
#             writer = csv.writer(file)
#             writer.writerow(["Name", "Date", "Time"])


# def already_marked_today(name):
#     """
#     Returns True if attendance for this person
#     has already been marked today.
#     """

#     initialize_attendance_file()

#     today = datetime.now().strftime("%Y-%m-%d")

#     with open(ATTENDANCE_FILE , 'r',newline="") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             if (row['Name']==name and row['Date']==today) :
#                 return True
#     return False

# def mark_attendence(name):
#     """
#     Marks attendance if not already marked today.
#     """

#     initialize_attendance_file()

#     if already_marked_today(name):
#         print(f"{name} already marked today.")
#         return False
    
#     now = datetime.now()

#     with open(ATTENDANCE_FILE , 'a',newline="") as file:
#         writer = csv.writer(file)

#         writer.writerow([name,now.strftime("%Y-%m-%d"),now.strftime("%H:%M:%S")])
    
#     print(f"Attendence Marked for {name}")

#     return True

# def get_attendence():

#     initialize_attendance_file()

#     records = []

#     with open(ATTENDANCE_FILE,'r',newline="") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             records.append(row)
    
#     return records