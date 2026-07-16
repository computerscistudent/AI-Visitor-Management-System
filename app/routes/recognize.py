from flask import Blueprint, render_template, Response
import cv2
import time

from app.services.recognition_service import (
    load_embeddings,
    recognize_faces
)

recognize_bp = Blueprint("recognize", __name__)

stop_camera = False 

def generate_frames():
    global stop_camera
    known_embeddings = load_embeddings()
    
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    if not camera.isOpened():
        raise RuntimeError("Could not start camera.")
    try:
        frame_count = 0
        faces = []
        stop_camera = False
        while True:
            if stop_camera:
                break
            success, frame = camera.read()

            if not success:
                print("Camera did not open")
                continue
            frame_count += 1
            if frame_count%2 == 0:
                faces = recognize_faces(frame, known_embeddings)

            for face in faces:
                x1, y1, x2, y2 = face["bbox"]

                cv2.rectangle(frame,(x1, y1),(x2, y2),(46, 204, 113),2)

                cv2.putText(
                    frame,
                    f"{face['name']} ({face['confidence']:.2f})",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            ret, buffer = cv2.imencode(".jpg", frame,[int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ret:
                continue
            frame = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame +
                b"\r\n"
            )
    finally :
        if camera is not None:
            camera.release()
            camera = None


@recognize_bp.route("/recognize")
def recognize():
    return render_template("recognize.html")


@recognize_bp.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@recognize_bp.route("/stop_camera")
def stop_camera_route():
    global stop_camera

    stop_camera = True

    return render_template("recognize_stopped.html")













# from flask import Blueprint, render_template, Response
# import cv2
# import time

# from app.services.recognition_service import (
#     load_embeddings,
#     recognize_faces
# )

# recognize_bp = Blueprint("recognize", __name__)

# # camera = None

# def generate_frames():
#     #global camera
#     known_embeddings = load_embeddings()
    
#     camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#     if not camera.isOpened():
#         raise RuntimeError("Could not start camera.")
#     try:
#         frame_count = 0
#         faces = []
#         while True:
#             success, frame = camera.read()

#             if not success:
#                 time.sleep(0.01)
#                 continue
#             frame_count += 1
#             if frame_count%2 == 0:
#                 faces = recognize_faces(frame, known_embeddings)

#             for face in faces:
#                 x1, y1, x2, y2 = face["bbox"]

#                 cv2.rectangle(frame,(x1, y1),(x2, y2),(46, 204, 113),2)

#                 cv2.putText(
#                     frame,
#                     f"{face['name']} ({face['confidence']:.2f})",
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.8,
#                     (0, 255, 0),
#                     2
#                 )

#             ret, buffer = cv2.imencode(".jpg", frame,[int(cv2.IMWRITE_JPEG_QUALITY), 80])
#             if not ret:
#                 continue
#             frame = buffer.tobytes()

#             yield (
#                 b"--frame\r\n"
#                 b"Content-Type: image/jpeg\r\n\r\n"
#                 + frame +
#                 b"\r\n"
#             )
#             time.sleep(0.03)
#     finally :
#         if camera is not None:
#             camera.release()
#             camera = None


# @recognize_bp.route("/recognize")
# def recognize():
#     return render_template("recognize.html")


# @recognize_bp.route("/video_feed")
# def video_feed():
#     return Response(
#         generate_frames(),
#         mimetype="multipart/x-mixed-replace; boundary=frame"
#     )