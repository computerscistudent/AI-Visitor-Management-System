from flask import Blueprint, render_template
from app.config import ATTENDANCE_FILE
import csv
import os

attendence_bp = Blueprint("attendence", __name__)

csv_file = ATTENDANCE_FILE

@attendence_bp.route("/attendence")
def attendence():
    records = []

    if os.path.exists(csv_file):
        with open(csv_file, 'r',newline="") as file:
            reader = csv.reader(file)
            next(reader,None)
            for row in reader:
                records.append(row)
    
    return render_template("attendence.html",records=records)

