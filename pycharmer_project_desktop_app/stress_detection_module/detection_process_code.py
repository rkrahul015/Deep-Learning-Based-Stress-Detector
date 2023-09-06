from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import datetime
from keras_preprocessing.image import img_to_array
from keras.models import load_model
import requests
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-at", "--access-token")
args = vars(ap.parse_args())

def eye_brow_distance(leye,reye):
    global points
    distq = dist.euclidean(leye,reye)
    points.append(int(distq))
    return distq

def emotion_finder(faces,frame):
    global emotion_classifier
    EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised","neutral"]
    x,y,w,h = face_utils.rect_to_bb(faces)
    frame = frame[y:y+h,x:x+w]
    if frame == []:
        return ""
    roi = cv2.resize(frame,(64,64))
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi,axis=0)
    preds = emotion_classifier.predict(roi)[0]
    emotion_probability = np.max(preds)
    label = EMOTIONS[preds.argmax()]
    if label in ['scared','sad']:
        label = 'stressed'
    else:
        label = 'not stressed'
    return label

def normalize_values(points,disp):
    normalized_value = abs(disp - np.min(points))/abs(np.max(points) - np.min(points))
    stress_value = np.exp(-(normalized_value))
    print(stress_value)
    if stress_value>=70:
        return stress_value,"High Stress"
    else:
        return stress_value,"low_stress"
    

#get the location of the eyes
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    eye_opening_ratio = (A + B) / (2.0 * C) 
    return eye_opening_ratio

ar_thresh = 0.3
eye_ar_consec_frame = 5
counter = 0
total = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/mukesh/hackfest/py_charmer_hackfest_project/pycharmer_project_desktop_app/stress_detection_module/shape_predictor_68_face_landmarks.dat")
emotion_classifier = load_model("/home/mukesh/hackfest/py_charmer_hackfest_project/pycharmer_project_desktop_app/stress_detection_module/_mini_XCEPTION.102-0.66.hdf5", compile=False)
cap = cv2.VideoCapture(0)
points = []
stress_lst = []
t1 = time.time()
t2 = time.time()
runner_index = 0 
last_total_blink_count = 0 
while(True):
    try:
        _,frame = cap.read()
        frame = cv2.flip(frame,1)
        frame = imutils.resize(frame, width=500,height=500)
    
    
        (lBegin, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
        (rBegin, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
        (lBegin_eye, lEnd_eye) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rBegin_eye, rEnd_eye) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        #preprocessing the image
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
        detections = detector(gray,0)
        for detection in detections:
            emotion = emotion_finder(detection,gray)
            shape = predictor(frame,detection)
            shape = face_utils.shape_to_np(shape)         
            leyebrow = shape[lBegin:lEnd]
            reyebrow = shape[rBegin:rEnd]
            
            reyebrowhull = cv2.convexHull(reyebrow)
            leyebrowhull = cv2.convexHull(leyebrow)

            cv2.drawContours(frame, [reyebrowhull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [leyebrowhull], -1, (0, 255, 0), 1)
            distq = eye_brow_distance(leyebrow[-1],reyebrow[0])
            stress_value,stress_label = normalize_values(points,distq)
            cv2.putText(frame, "Stressed " if int(stress_value * 100) >= 70 else "Not Stressed", (10,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if int(stress_value * 100) <= 70  else (0, 0, 255), 2)
            cv2.putText(frame,"stress level:{}".format(str(int(stress_value*100))),(20,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if int(stress_value * 100) <= 70 else (0, 0, 255), 2)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_image = clahe.apply(gray)
        detections = detector(clahe_image,0)
        for detection in detections:
            shape = predictor(gray,detection)
            shape = face_utils.shape_to_np(shape)
            left_eye = shape[lBegin_eye:lEnd_eye]
            right_eye = shape[rBegin_eye:rEnd_eye]
            leftEyeHull = cv2.convexHull(left_eye)
            rightEyeHull= cv2.convexHull(right_eye)
            cv2.drawContours(clahe_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(clahe_image, [rightEyeHull], -1, (0, 255, 0), 1)
            #calculating the EAR
            left_eye_Ear = eye_aspect_ratio(left_eye)
            right_eye_Ear = eye_aspect_ratio(right_eye)

            avg_Ear = (left_eye_Ear + right_eye_Ear)/2.0

            if avg_Ear<ar_thresh:
                counter+=1
            else:
                if counter>eye_ar_consec_frame:
                    total+= 1
                counter = 0	
            cv2.putText(clahe_image, "Blinks: {}".format(total), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(clahe_image, "EAR: {:.2f}".format(avg_Ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Blink count", clahe_image)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        stress_lst.append(int(stress_value * 100))
        t2 = time.time()
        if t2 - t1 >= 60:
            t1 = t2
            stress_values = stress_lst[runner_index:]
            runner_index = len(stress_lst) - 1
            blink_count = total - last_total_blink_count
            last_total_blink_count = total
            req_body = {
                'access_token': args['access_token'],
                'stress_list_lst': stress_values,
                'blink_count': blink_count,
                'timestamp': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
            res = requests.post("http://127.0.0.1:8080/stress_blink_value/add_stress_blink_values", json = req_body)
        if key == ord('q'):
            break
    except Exception as e:
        print(e)
cv2.destroyAllWindows()
cap.release()
