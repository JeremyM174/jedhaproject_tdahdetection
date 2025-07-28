import cv2
from PIL import Image
import time
from collections import deque, Counter
from dotenv import load_dotenv
import warnings

import cnn
import llm

load_dotenv()
warnings.filterwarnings("ignore")



def showfps(frame, prev_frame_time):
    """Performance measure (camera+computation) should we want to restrict and stabilize CNN input, displayed while capturing user."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    fps = str(round(fps))
    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    return new_frame_time



def get_response_from_cnn(frame):
    """Core function communicating both ways with our CNN. For **each** frame:
    * Captured frame (np.array format) is transformed into a PIL image sent as CNN input,\n
    * CNN returns float values as output representing how strong emotions were recognized,\n
    * Said values are then matched to their labels, so we may extract the most representative one into a list 'history'.\n
    Given the focus on ADHD, very low engagement (='disengagement' emotion) is given priority in recognition.\n
    Amongst the other three, only the top representative is kept. All other cases stored as 'incertitude' to be ignored by LLM requests."""

    pilimage = Image.fromarray(frame).convert("RGB")
    cnn_predict = (cnn.get_emotion(pilimage))[0].tolist()
    #print(cnn_predict) #sanity check
    dict_cnn = {"boredom" : cnn_predict[0], "engagement" : cnn_predict[1], "confusion" : cnn_predict[2], "frustration" : cnn_predict[3]}
    cnn_engagement = dict_cnn.pop("engagement")
    cnn_bcf = max(dict_cnn.values())

    if cnn_engagement < 1:
        return "disengagement"
    elif cnn_bcf > 2 and cnn_engagement >= 1:
        return max(dict_cnn, key=dict_cnn.get)
    else:
        return "incertitude"



def evaluate_response(history):
    """Takes as input the real-time updating list 'history', to extract the most recurrent emotion over last frames ('deque_length').\n
    Output will determine whether to call or not the LLM for a recommendation."""
    return Counter(history).most_common(1)[0][0]



cap = cv2.VideoCapture(0)
prev_frame_time = 0
new_frame_time = 0
deque_length = 100
history = deque([], maxlen=deque_length)
last_action_time = time.time()

while( cap.isOpened() ):
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame,1)
        prev_frame_time = showfps(frame, prev_frame_time)

        cnnresponse = get_response_from_cnn(frame)
        #print(cnnresponse) #sanity check
        history.append(cnnresponse)

        if len(history) == deque_length:
            action = evaluate_response(history)

            if time.time() - last_action_time >= 10 and not action=="incertitude":
                last_action_time = time.time()
                #print(action) #sanity check
                message = llm.get_recommendation(action)
                print(message)

        cv2.imshow('frame' , frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()