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

# --- Définition de la fonction pour le slider à usage unique ---
def single_use_slider(key_prefix: str = "default_slider", title: str = "Sélectionnez une valeur", options=None):
    """
    Affiche un slider Streamlit qui peut être utilisé une seule fois.
    Une fois la valeur confirmée, le slider disparaît et la valeur est affichée.

    Args:
        key_prefix (str): Préfixe pour les clés de session et de widget pour éviter les conflits.
        title (str): Le titre à afficher au-dessus du slider.
        options (list): La liste des options pour le select_slider.
    """
    if options is None:
        # Options par défaut si non fournies
        options = [f"{i:02d}:00" for i in range(24)]

    # Initialisation de l'état de la session, spécifique à cette instance de slider
    # Utilisez le préfixe pour que chaque instance de slider ait son propre état
    confirmed_key = f"{key_prefix}_confirmed_value"
    disabled_key = f"{key_prefix}_disabled"

    if confirmed_key not in st.session_state:
        st.session_state[confirmed_key] = None
    if disabled_key not in st.session_state:
        st.session_state[disabled_key] = False

    # Afficher le slider UNIQUEMENT si la valeur n'a pas encore été confirmée
    if not st.session_state[disabled_key]:
        st.write(f"Veuillez {title.lower()} et confirmer :")
        selected_value = st.select_slider(
            title,
            options=options,
            key=f"{key_prefix}_slider_widget" # Clé unique pour le widget
        )

        # Bouton de confirmation
        if st.button(f'Confirmer {title.lower().replace("sélectionnez ", "")}', key=f"{key_prefix}_confirm_button"):
            st.session_state[confirmed_key] = selected_value
            st.session_state[disabled_key] = True
            st.rerun() # Recharger l'application pour appliquer les changements d'état
    else:
        # Une fois la valeur confirmée, affichez uniquement la valeur choisie et un message
        st.success(f"{title.replace('Sélectionnez une', 'Valeur')} confirmée : **{st.session_state[confirmed_key]}**")
        st.write(f"Le {title.lower()} a disparu.")

    # Retourne la valeur confirmée (ou None si pas encore confirmée)
    return st.session_state[confirmed_key]

# --- Fin de la définition de la fonction ---

# === Interface Streamlit ===

st.set_page_config(page_title="ADHD Emotion Tracker", layout="wide")
st.title("🧠 ADHD Emotion Recognition & Recommendation")

# --- Intégration du slider à usage unique ---
st.header("Section B : Sélection de temps unique")
# Appeler la fonction pour le slider à usage unique
# Utilisez un préfixe de clé unique pour cette instance
selected_time_confirmed = single_use_slider(
    key_prefix="time_selection",
    title="Sélectionnez une minutes",
    options=[f"{i:02d}" for i in range(0,120,15)]
)

if selected_time_confirmed:
    st.info(f"Le temps choisi pour cette section est : {selected_time_confirmed}")

# --- Bouton de réinitialisation global (optionnel) ---
# Ce bouton permet de remettre TOUTES les instances de single_use_slider à leur état initial pour les tests
# C'est un peu plus complexe si vous avez plusieurs instances du slider unique,
# car il faudrait itérer sur toutes les clés de session.
# Pour simplifier, nous allons juste montrer comment réinitialiser la dernière instance.
if st.button('Réinitialiser la dernière sélection de temps'):
    st.session_state["time_selection_confirmed_value"] = None
    st.session_state["time_selection_disabled"] = False
    # st.cache()
    st.rerun()


# ==== Run du CNN + LLm =======

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
            # cv2.putText(annotated_frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)
            # cv2.putText(annotated_frame, f"Emotion: {emotion}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

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

