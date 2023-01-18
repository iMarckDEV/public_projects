import boto3
import os
import cv2
import dlib
import time
from scipy.spatial import distance as dist
import numpy as np
import json


s3_client = boto3.client('s3')

def eye_aspect_ratio(eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear


def handler(event, context):
    #funciona por un json que contenga bucket y obj_key
    #o por un evento s3

    bk0 = event.get("bucket", None)
    pth0 = event.get("obj_key", None)

    if bk0==None or pth0==None:
        ####evento
        object_key = event["Records"][0]["s3"]["object"]["key"]
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
    
        object_key=str(object_key) ###casteo a string por si acaso
    else:
        object_key=str(pth0)
        bucket=str(bk0)
    
    ####extraer el nombre del archivo
    if '/' in object_key:
        archivo_name=object_key.split('/')
        archivo_name=archivo_name[len(archivo_name)-1] ###archivo.png
    else:
        archivo_name=object_key

    print('PROCESANDO:{}'.format(archivo_name))

    download_path='/tmp/{}'.format(archivo_name) ##RUTA PARA LA IMAGEN
    #upload_path = '/tmp/resized-{}'.format(archivo_name)##RESIZE PARA IMAGEN

    s3_client.download_file(bucket, object_key, download_path)##COPIAR EL ARCHIVO


   

    # thresholds and initializations
    EYE_ASPECT_RATIO_THRESHOLD = 0.3
    EYE_ASPECT_RATIO_CONSEC_FRAMES = 3
    COUNTER = 0
    TOTAL = 0
    BLINK_COUNTER = 0
    start_time = time.time()
    blink_start_time = 0

    cwd = os.getcwd()

    # dlib face and landmark predictors
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(f'{cwd}/shape_predictor_68_face_landmarks.dat')



    # indexes for left and right eye
    (lStart, lEnd) = (42, 48)
    (rStart, rEnd) = (36, 42)

    # start video stream
    

    #vs = cv2.VideoCapture(0)
    vs = cv2.VideoCapture(download_path)

    pic_name='FRAME_VIDEO'

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
        # If a minute has passed
        if elapsed_time > 60:
            print('Blinks per minute:', BLINK_COUNTER)
            BLINK_COUNTER = 0
            start_time = time.time()

        if BLINK_COUNTER>2:
            #save the frame
            cv2.imwrite(f'/tmp/{pic_name}.jpg', frame)

    #print('PLACA:{}, DATA:{}'.format(placa,text))
    #r_img.save('/tmp/scaled_{}'.format(archivo_name))
    s3_client.upload_file(f'/tmp/{pic_name}.jpg', bucket, f'/tmp/{pic_name}.jpg')##COPIAR EL ARCHIVO

    os.remove(download_path) 
    os.remove(f'/tmp/{pic_name}.jpg') 
        
    ##    resize_image(download_path, upload_path)
    #s3_client.upload_file(upload_path, 'mloaiza.test','rs-{}'.format(key))

    r={'blinks pm': BLINK_COUNTER}

    return {
        'statusCode':200,
        'body':json.dumps(r)}

