import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import time
from collections import deque, Counter
from PIL import Image
from queue import Queue, Empty
import threading
import warnings
from dotenv import load_dotenv

import cnn
import llm

load_dotenv()
warnings.filterwarnings("ignore")

# Queue thread-safe pour passer les frames
frame_queue = Queue(maxsize=1)

# Historique pour 10 dernières secondes
emotion_history = deque(maxlen=10)

# Etat partagé
shared_state = {"current_emotion": "Aucune", "messages": [], "last_mean_time": 0}


def get_response_from_cnn(frame):
    pilimage = Image.fromarray(frame).convert("RGB")
    cnn_predict = (cnn.get_emotion(pilimage))[0].tolist()
    print("cnn_predict:", cnn_predict)

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


def cnn_worker():
    frame_count = 0
    while True:
        try:
            frame = frame_queue.get(timeout=1)
        except Empty:
            continue

        frame_count += 1
        # Traiter une frame par seconde (environ 30 fps -> 1 sur 30)
        if frame_count % 30 != 0:
            continue

        print("Traitement CNN sur une frame")
        emotion = get_response_from_cnn(frame)
        emotion_history.append(emotion)
        shared_state["current_emotion"] = emotion

        now = time.time()
        if len(emotion_history) == 10 and (now - shared_state["last_mean_time"] >= 10):
            shared_state["last_mean_time"] = now
            dominant = Counter(emotion_history).most_common(1)[0][0]
            shared_state["messages"].append(f"Émotion dominante sur 10s : {dominant}")
            print(f"[10s] Émotion dominante : {dominant}")


# Lancer le thread CNN une seule fois
if "cnn_thread_started" not in st.session_state:
    threading.Thread(target=cnn_worker, daemon=True).start()
    st.session_state.cnn_thread_started = True


# Processor vidéo
class EmotionProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Mettre la frame dans la queue sans bloquer
        if frame_queue.empty():
            frame_queue.put_nowait(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# UI Streamlit
st.title("Détection émotionnelle (queue multithread)")

popups_placeholder = st.empty()
status_placeholder = st.empty()

webrtc_streamer(
    key="emotion",
    video_processor_factory=EmotionProcessor,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={
        "video": {
            "width": {"ideal": 1280},
            "height": {"ideal": 720},
            "frameRate": {"ideal": 30},
        },
        "audio": False,
    },
    video_html_attrs={"style": {"width": "100%"}, "controls": False, "autoPlay": True},
)

status_placeholder.info(f"Émotion actuelle : {shared_state['current_emotion']}")

if shared_state["messages"]:
    for msg in shared_state["messages"][-3:]:
        popups_placeholder.warning(msg)
