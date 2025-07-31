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

# --- La personnalisation du streamlit ---
custom_css = """
<style>
/* Changer la couleur des titres H1 */
h1 {
    color: #4BE8E0; /* Un turquoise vibrant */
    text-align: center; /* Ajouté pour centrer le titre H1 */
}

/* Changer la couleur des titres H2 */
h2 {
    color: #23B1AB; /* Un autre turquoise/bleu vert */
}

/* Cibler les boutons Streamlit */
.stButton>button {
    background-color: #2A7FAF; /* Couleur de fond du bouton */
    color: white; /* Couleur du texte du bouton */
}

/* Cibler les liens */
a {
    color: #9DD4F3; /* Bleu clair pour les liens */
}

/* Style pour l'encart central de Wakee */
.wakee-message-container {
    background-color: #015955; /* Couleur de fond de secondaryBackgroundColor */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    text-align: center;
    margin-top: 20px; /* Ajoute un peu d'espace au-dessus */
}
.wakee-message-container h3 {
    color: #97FBF6; /* Une couleur claire pour le titre de l'encart */
    font-size: 1.8em; /* Augmente la taille du titre de l'encart */
    margin-bottom: 15px; /* Espace sous le titre */
}
/* Style pour le message du LLM à l'intérieur de l'encart */
.llm-output-text {
    color: #FFFFFF; /* Texte blanc */
    font-size: 1.6em; /* **Taille plus grosse pour le message LLM** */
    font-weight: bold; /* Texte en gras pour plus d'impact */
    line-height: 1.4; /* Espace entre les lignes pour la lisibilité */
}

/* Centrer le contenu des colonnes pour un alignement visuel plus agréable */
.stColumn {
    display: flex;
    flex-direction: column;
    align-items: center; /* Centre le contenu horizontalement dans les colonnes */
    text-align: center; /* Centre le texte si besoin */
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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
    if not history:
        return "incertitude"
    return Counter(history).most_common(1)[0][0]

# --- Définition de la fonction pour le slider à usage unique ---
def single_use_slider(key_prefix: str = "default_slider", title: str = "Sélectionnez une valeur", options=None):
    if options is None:
        options = [f"{i:02d}:00" for i in range(24)]

    confirmed_key = f"{key_prefix}_confirmed_value"
    disabled_key = f"{key_prefix}_disabled"

    if confirmed_key not in st.session_state:
        st.session_state[confirmed_key] = None
    if disabled_key not in st.session_state:
        st.session_state[disabled_key] = False

    if not st.session_state[disabled_key]:
        st.write(f"Je choisis mon temps de travail et je confirme.")
        selected_value = st.select_slider(
            title,
            options=options,
            key=f"{key_prefix}_slider_widget"
        )

        if st.button(f'Confirmer mon temps de travail', key=f"{key_prefix}_confirm_button"):
            st.session_state[confirmed_key] = selected_value
            st.session_state[disabled_key] = True
            st.rerun()
    else:
        st.success(f"Je vais travailler pendant **{st.session_state[confirmed_key]}** min. C'est parti !")

    return st.session_state[confirmed_key]


# === Interface Streamlit ===

st.set_page_config(page_title="WAKEE", layout="wide")

# Titres principaux centrés
st.markdown("<h1 style='text-align: center; color: #4BE8E0;'>Je travaille avec WAKEE !</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #23B1AB;'>Reconnaissance des émotions & Recommendation pour le TDAH 🧠</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FFFFFF;'>🤖 W.A.K.E.E. : Work Assistant with Kindness & Emotional Empathy 🤗</p>", unsafe_allow_html=True)
st.markdown("---")

# Création des colonnes : une pour le choix du temps (col1) et une pour la caméra (col2)
col1, col_spacer, col2 = st.columns([0.3, 0.05, 0.65])

with col1:
    st.markdown("<h3 style='text-align: center; color: #23B1AB;'>⏱️ Choix du temps de travail</h3>", unsafe_allow_html=True)

    selected_time_confirmed = single_use_slider(
        key_prefix="time_selection",
        title="Combien de temps je veux travailler (en minutes) : ",
        options=[f"{i:02d}" for i in range(15, 135, 15)]
    )

    if selected_time_confirmed:
        st.info("Je peux allumer ma caméra et démarrer ma session 🦾​")

    if st.button('Réinitialiser & changer mon temps de travail'):
        st.session_state["time_selection_confirmed_value"] = None
        st.session_state["time_selection_disabled"] = False
        # Réinitialise aussi le temps de début de la session pour la barre de progression
        st.session_state.start_time = None
        st.rerun()

    # --- Barre de progression du temps de travail ---
    st.markdown("<h3 style='text-align: center; color: #23B1AB;'>⌛ Temps écoulé</h3>", unsafe_allow_html=True)
    # Placeholder pour la barre de progression et le texte associé
    progress_bar_placeholder = st.empty()
    progress_text_placeholder = st.empty()


with col2:
    st.markdown("<h3 style='text-align: center; color: #23B1AB;'>🎥 Ma camera</h3>", unsafe_allow_html=True)

    start_button = st.toggle("Activer ma camera 🔴​")

    # Containers dynamiques pour la caméra et les stats
    image_display = st.empty()
    stats_display = st.empty()
    emotion_display = st.empty()

# --- Encart central pour Wakee ---
col_left_center, col_center_content, col_right_center = st.columns([0.2, 0.6, 0.2])

with col_center_content:
    llm_container_placeholder = st.empty()

# --- Fonction pour générer le HTML de l'encart Wakee ---
def render_wakee_message_container(message: str):
    return f"""
    <div class="wakee-message-container">
        <h3>💬 Suggestions de Wakee :</h3>
        <p class="llm-output-text">{message}</p>
    </div>
    """

# --- Logique de la caméra et du LLM ---

# Initialisation du temps de début de la session dans st.session_state
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if start_button:
    # Si la caméra vient d'être activée, enregistre le temps de début
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
        st.session_state.time_remaining_message_sent = False # Flag to send completion message once

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("⚠️ Impossible d'accéder à la caméra.")
    else:
        # Message initial au démarrage de la caméra
        current_llm_message = "Prêt à t'aider ! J'analyse tes émotions et je t'aiderais au besoin 😊​"
        llm_container_placeholder.markdown(render_wakee_message_container(f'💬 {current_llm_message}'), unsafe_allow_html=True)

        # S'assurer que selected_time_confirmed est un nombre (convertir de string "XX")
        total_work_time_minutes = int(selected_time_confirmed) if selected_time_confirmed else 0
        total_work_time_seconds = total_work_time_minutes * 60

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

            # --- Mise à jour de la barre de progression ---
            elapsed_time_seconds = time.time() - st.session_state.start_time
            
            if total_work_time_seconds > 0:
                progress_percentage = min(elapsed_time_seconds / total_work_time_seconds, 1.0)
            else:
                progress_percentage = 0.0 # Si 0 minutes sont choisies, la progression reste à 0

            # Mettre à jour la barre et le texte
            progress_bar_placeholder.progress(progress_percentage)
            
            remaining_seconds = max(0, total_work_time_seconds - elapsed_time_seconds)
            mins = int(remaining_seconds // 60)
            secs = int(remaining_seconds % 60)
            
            progress_text_placeholder.text(f"Temps restant : {mins:02d}m {secs:02d}s")

            # Condition pour vérifier si le temps est écoulé
            if elapsed_time_seconds >= total_work_time_seconds and total_work_time_seconds > 0 and not st.session_state.time_remaining_message_sent:
                llm_container_placeholder.markdown(render_wakee_message_container("Félicitations ! Votre temps de travail est terminé. Prenez une pause bien méritée ! 🎉"), unsafe_allow_html=True)
                st.session_state.time_remaining_message_sent = True # Empêche le message de se répéter

            # Affichage de l'image et des stats dans les colonnes de la caméra
            with col2:
                image_display.image(rgb_frame, channels="RGB")
                stats_display.markdown(f"**🧮 Frame :** {frame_count}  |  **⚡ FPS :** {fps}")
                emotion_display.markdown(f"**🧠 Dernière émotion détectée :** `{emotion}`")

            # Détection LLM et mise à jour de l'encart central
            if len(history) == deque_length:
                action = evaluate_response(history)
                history.clear()

                if time.time() - last_action_time >= 10 and action != "incertitude":
                    last_action_time = time.time()
                    message = llm.get_recommendation(action)
                    current_llm_message = message
                elif action == "incertitude":
                    current_llm_message = "Je ne suis pas sûr de ce que tu ressens. Continue !"
                else:
                    current_llm_message = "Tout va bien pour l'instant ! 😎​"

            # Mise à jour du placeholder de l'encart complet (sauf si le message de fin a été envoyé)
            if not st.session_state.get("time_remaining_message_sent", False):
                llm_container_placeholder.markdown(render_wakee_message_container(f'{current_llm_message}'), unsafe_allow_html=True)

            time.sleep(FRAME_SKIP_SECONDS)

        cap.release()
else: # Si la caméra est désactivée
    image_display.empty()
    stats_display.empty()
    emotion_display.empty()
    
    # Réinitialise la barre de progression et le texte
    progress_bar_placeholder.progress(0)
    progress_text_placeholder.text("Temps restant : 00m 00s")
    
    # Réinitialise le temps de début de la session
    st.session_state.start_time = None
    st.session_state.time_remaining_message_sent = False

    # Afficher le message initial dans l'encart quand la caméra n'est pas activée
    llm_container_placeholder.markdown(render_wakee_message_container("Démarre ta session en activant la caméra ci-dessus ⬆️​ 👍​"), unsafe_allow_html=True)

# --- Section Crédits ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; color: #CCCCCC;">
        <p>Développé avec 💙 par :</p>
        <p><strong> Albert ROMANO, Asma RHALMI, Jeremy MARIARGE, Manon FAEDY </strong></p>
    </div>
    """,
    unsafe_allow_html=True
)