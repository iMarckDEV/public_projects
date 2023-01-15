import cv2
import dlib
import time
from scipy.spatial import distance as dist
import numpy as np
import os

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

work_dir = os.getcwd()

# thresholds and initializations
EYE_ASPECT_RATIO_THRESHOLD = 0.3
EYE_ASPECT_RATIO_CONSEC_FRAMES = 3
COUNTER = 0
TOTAL = 0
BLINK_COUNTER = 0
start_time = time.time()
blink_start_time = 0

# dlib face and landmark predictors
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(f'{work_dir}/shape_predictor_68_face_landmarks.dat')


# indexes for left and right eye
(lStart, lEnd) = (42, 48)
(rStart, rEnd) = (36, 42)

# start video stream
vs = cv2.VideoCapture(0) ##change 0 by the path of the video too

while True:
    ret, frame = vs.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    rects = detector(gray, 0)

    # for each detected face
    for rect in rects:
        shape = predictor(gray, rect)

        # get the coordinates of the left and right eyes
        leftEye = [(shape.part(i).x, shape.part(i).y) for i in range(lStart, lEnd)]
        rightEye = [(shape.part(i).x, shape.part(i).y) for i in range(rStart, rEnd)]

        # draw the eyes on the frame
        cv2.polylines(frame, [np.array(leftEye)], True, (0, 255, 0), 1)
        cv2.polylines(frame, [np.array(rightEye)], True, (0, 255, 0), 1)

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        if ear < EYE_ASPECT_RATIO_THRESHOLD:
            if COUNTER == 0:
                blink_start_time = time.time()  # Starting time of the blink
            COUNTER += 1
        else:
            if COUNTER >= EYE_ASPECT_RATIO_CONSEC_FRAMES:
                blink_duration = time.time() - blink_start_time  # Duration of the blink
                if blink_duration >= 0.5:  # Only count blinks where the eye is closed for 0.5 seconds or more
                    TOTAL += 1
                    BLINK_COUNTER += 1
            COUNTER = 0

    # Show blink count on the frame
    cv2.putText(frame, "Blinks: {}".format(BLINK_COUNTER), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Calculate elapsed time in seconds
    elapsed_time = time.time() - start_time
    
    # If a minute has passed
    if elapsed_time > 60:
        print('Blinks per minute:', BLINK_COUNTER)
        BLINK_COUNTER = 0
        start_time = time.time()

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.release()
