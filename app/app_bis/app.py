import streamlit as st
import cv2
import time
from PIL import Image
from collections import deque, Counter
from dotenv import load_dotenv
import warnings

import cnn
import llm

load_dotenv()
warnings.filterwarnings("ignore")


# --- Fonctions ---
def showfps(frame, prev_frame_time):
    new_frame_time = time.time()
    if prev_frame_time > 0:
        fps = 1 / (new_frame_time - prev_frame_time)
        cv2.putText(
            frame,
            str(round(fps)),
            (7, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (100, 255, 0),
            2,
            cv2.LINE_AA,
        )
    return new_frame_time


def get_response_from_cnn(frame):
    pilimage = Image.fromarray(frame).convert("RGB")
    cnn_predict = (cnn.get_emotion(pilimage))[0].tolist()
    dict_cnn = {
        "boredom": cnn_predict[0],
        "engagement": cnn_predict[1],
        "confusion": cnn_predict[2],
        "frustration": cnn_predict[3],
    }
    cnn_engagement = dict_cnn.pop("engagement")
    cnn_bcf = max(dict_cnn.values())

    if cnn_engagement < 1:
        return "disengagement"
    elif cnn_bcf > 2 and cnn_engagement >= 1:
        return max(dict_cnn, key=dict_cnn.get)
    else:
        return "incertitude"


def evaluate_response(history):
    return Counter(history).most_common(1)[0][0]


# --- State init ---
if "running" not in st.session_state:
    st.session_state.running = False
if "history" not in st.session_state:
    st.session_state.history = deque([], maxlen=100)
if "last_action_time" not in st.session_state:
    st.session_state.last_action_time = time.time()
if "prev_frame_time" not in st.session_state:
    st.session_state.prev_frame_time = 0
if "cap" not in st.session_state:
    st.session_state.cap = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # stocke les recommandations

# --- UI ---
col1, col2, col3 = st.columns([1, 1, 1])


def toggle_run():
    st.session_state.running = not st.session_state.running
    if st.session_state.running:
        st.session_state.cap = cv2.VideoCapture(0)
    else:
        if st.session_state.cap:
            st.session_state.cap.release()
        st.session_state.cap = None


with col1:
    st.button("Start/Stop", on_click=toggle_run)
with col2:
    st.markdown(
        "<div style='text-align:center;background:#ffcccc;padding:10px;border-radius:5px;'>ON AIR</div>",
        unsafe_allow_html=True,
    )
runtime_placeholder = col3.empty()

video_placeholder = st.empty()
popups_placeholder = st.empty()
objectifs_placeholder = st.empty()

# --- Main loop (une frame par reload) ---
if st.session_state.running and st.session_state.cap:
    ret, frame = st.session_state.cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        st.session_state.prev_frame_time = showfps(
            frame, st.session_state.prev_frame_time
        )

        # CNN
        cnnresponse = get_response_from_cnn(frame)
        st.session_state.history.append(cnnresponse)

        # Tous les 10s une recommandation
        if (
            len(st.session_state.history) == st.session_state.history.maxlen
            and time.time() - st.session_state.last_action_time >= 10
        ):
            action = evaluate_response(st.session_state.history)
            if action != "incertitude":
                st.session_state.last_action_time = time.time()
                message = llm.get_recommendation(action)
                st.session_state.messages.append(message)

        # Affichage vidéo
        video_placeholder.image(frame, channels="BGR")
        objectifs_placeholder.info("Objectifs : rester attentif et calme")
        runtime_placeholder.success(
            f"Run time : {int(time.time() - st.session_state.last_action_time)} s"
        )

# --- Affiche les recommandations même après avoir arrêté ---
if st.session_state.messages:
    for msg in st.session_state.messages[-3:]:
        popups_placeholder.warning(msg)
