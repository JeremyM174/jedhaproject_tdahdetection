import streamlit as st
import cv2
from PIL import Image
import time
from collections import deque, Counter
import numpy as np
import warnings
from dotenv import load_dotenv

import cnn  # ton module qui retourne les prédictions
import llm  # ton module LLM

warnings.filterwarnings("ignore")
load_dotenv()

# --- Paramètres ---
deque_length = 100
history = deque([], maxlen=deque_length)
last_action_time = time.time()
FRAME_SKIP_SECONDS = 0.1
prev_frame_time = 0
frame_count = 0

# === Fonctions ===
def showfps(prev_time):
    new_time = time.time()
    fps = 1 / (new_time - prev_time + 1e-8)
    return new_time, int(fps)

def get_response_from_cnn(frame):
    pilimage = Image.fromarray(frame).convert("RGB")
    cnn_predict = cnn.get_emotion(pilimage)[0].tolist()
    dict_cnn = {"boredom": cnn_predict[0], "engagement": cnn_predict[1],
                "confusion": cnn_predict[2], "frustration": cnn_predict[3]}
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

# === Interface Streamlit ===
st.set_page_config(page_title="ADHD Emotion Tracker", layout="wide")
st.title("🧠 ADHD Emotion Recognition & Recommendation")

start_button = st.toggle("🎥 Activer la Webcam")

# Containers dynamiques
image_display = st.empty()
stats_display = st.empty()
emotion_display = st.empty()
llm_display = st.empty()

if start_button:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("⚠️ Impossible d'accéder à la caméra.")
    else:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("❌ Erreur de lecture de la caméra.")
                break

            frame_count += 1
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            prev_frame_time, fps = showfps(prev_frame_time)
            emotion = get_response_from_cnn(rgb_frame)
            history.append(emotion)

            # Annotation sur l’image
            annotated_frame = rgb_frame.copy()
            cv2.putText(annotated_frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
            cv2.putText(annotated_frame, f"Emotion: {emotion}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Affichage
            image_display.image(annotated_frame, channels="RGB")
            stats_display.markdown(f"**🧮 Frame :** {frame_count}  |  **⚡ FPS :** {fps}")
            emotion_display.markdown(f"**🧠 Dernière émotion détectée :** `{emotion}`")

            # Détection LLM
            if len(history) == deque_length:
                action = evaluate_response(history)

                if time.time() - last_action_time >= 10 and action != "incertitude":
                    last_action_time = time.time()
                    message = llm.get_recommendation(action)
                    llm_display.markdown(f"💬 **LLM Suggestion pour `{action}` :** {message}")

            time.sleep(FRAME_SKIP_SECONDS)
        cap.release()