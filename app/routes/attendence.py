from flask import Blueprint, render_template,request,send_file, Response
from app.services.attendance_service import get_attendance
import csv
import io

attendence_bp = Blueprint("attendence", __name__)

@attendence_bp.route("/attendence")
def attendence():
    sort = request.args.get("sort", "newest")
    records = get_attendance()

    if sort == "newest":
         records.sort(key=lambda x: (x['Date'], x['Time']), reverse=True)

    elif sort == "oldest":
         records.sort(key=lambda x: (x['Date'], x['Time']))

    elif sort == "name":
         records.sort(key=lambda x: x['Name'].lower())

    return render_template("attendence.html",records=records,sort=sort)


@attendence_bp.route("/download")
def download():
    records = get_attendance()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Name","Date","Time"])

    for row in records:
        writer.writerow([row['Name',row['Date'],row['Time']]])

    output.seek(0)
    
    return Response(
        output.getvalue(),mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=attendance.csv"
        }
    )






# csv_file = ATTENDANCE_FILE

# @attendence_bp.route("/attendence")
# def attendence():
#     sort = request.args.get("sort", "newest")
#     records = []

#     if os.path.exists(csv_file):
#         with open(csv_file, 'r',newline="") as file:
#             reader = csv.reader(file)
#             next(reader,None)
#             for row in reader:
#                 name = row[0]
#                 image = "img_001.jpg"
#                 records.append({
#                     "name": row[0],
#                     "date": row[1],
#                     "time": row[2],
#                     "image": image
#                 })
#     if sort == "newest":
#         records.sort(key=lambda x: (x['date'], x['time']), reverse=True)

#     elif sort == "oldest":
#         records.sort(key=lambda x: (x['date'], x['time']))

#     elif sort == "name":
#         records.sort(key=lambda x: x['name'].lower())

#     return render_template("attendence.html",records=records,sort=sort)

# @attendence_bp.route("/download")
# def download():
#     return send_file(
#         csv_file,
#         as_attachment=True,
#         download_name="attendence.csv"
#     )