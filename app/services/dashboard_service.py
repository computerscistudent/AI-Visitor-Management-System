import os
from datetime import datetime
from app.config import DATASET_DIR
from app.services.attendance_service import get_attendance

def total_registered_visitors()-> int:
    if not os.path.exists(DATASET_DIR):
        return 0
    count = 0
    for folder in os.listdir(DATASET_DIR):
        if os.path.isdir(os.path.join(DATASET_DIR,folder)):
            count += 1
    
    return count


def attendence_today():
    today = datetime.now().strftime("%Y-%m-%d")
    records = get_attendance()

    sum = 0
    for row in records:
        if row["Date"]==today:
           sum += 1

    return sum 

