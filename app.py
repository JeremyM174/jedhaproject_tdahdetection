import numpy
import cv2
from PIL import Image
import time
from collections import deque, Counter
import os
from dotenv import load_dotenv
import warnings

import cnn
import llm

# !!! remember to insert Mistral API key as environment variable !!!
load_dotenv()
warnings.filterwarnings("ignore")

def showfps(frame, prev_frame_time):
    font = cv2.FONT_HERSHEY_SIMPLEX
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    fps = str(round(fps))
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    return new_frame_time

def get_response_from_cnn(frame):
    pilimage = Image.fromarray(frame).convert("RGB")
    cnn_predict = (cnn.get_emotion(pilimage))[0].tolist()
    dict_cnn = {"boredom" : cnn_predict[0], "engagement" : cnn_predict[1], "confusion" : cnn_predict[2], "frustration" : cnn_predict[3]}
    cnn_engagement = dict_cnn.pop("engagement")
    cnn_bcf = max(dict_cnn.values())

    if cnn_bcf > 2 and cnn_engagement >= 1:
        return max(dict_cnn, key=dict_cnn.get)
    elif cnn_engagement < 1:
        return "disengagement"
    else:
        return "incertitude"



def evaluate_response(history):
    return Counter(history).most_common(1)[0][0]



cap = cv2.VideoCapture(0)
prev_frame_time = 0
new_frame_time = 0
deq_len = 100
history = deque([], maxlen=deq_len)
last_action_time = time.time()

while( cap.isOpened() ):
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame,1)
        prev_frame_time = showfps(frame, prev_frame_time)

        cnnresponse = get_response_from_cnn(frame)
        print(cnnresponse)
        ###stop calcul
        history.append(cnnresponse)

        if len(history) == deq_len:
            action = evaluate_response(history)

            if time.time() - last_action_time >= 10 and not action=="incertitude":
                last_action_time = time.time()
                print(action)
                message = llm.get_recommendation(action)
                print(message)

        cv2.imshow('frame' , frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()