import streamlit as st
import time

#popover pour demander le temps de travail
with st.popover("Definir mon temps de travail"):
    workduration = st.text_input("Pendant combien de temps est ce que je compte travailler ?")
st.write("Your name:", workduration)

# Single-select segmented control bouton de lancement du travail
option_map = {
    0: "Let's start working",
    1: "Taking a break",
    2: "Ending work"
}
selection = st.segmented_control(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)

#lancement d'une boucle if si on a cliqué sur le bouton "Let's start working"
# (rajouter une condition pour s'il n'y a pas de temps de travail de rentré ?)
if selection == 0:

    # spinner de chargement avec affichage du statut à la fin
    with st.spinner("Wait for it...", show_time=True):
        #lignes de lancement de la camera


    st.success("Camera active !")

    # bar de progression à lier avec le temps
    progress_text = "Work in progress. Keep going !."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100): #faire avec workduration mais l'afficher en % ?
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)

        # la que tout notre code cnn + llm se place ?

        #toast
        if message_llm == True:
            st.toast(message_llm)

    time.sleep(1)
    my_bar.empty()



elif selection == 1:
    #faire une pause du code
    #faire une pause de la camera sur le même endroit que le précédent message ?
    # faire une pause du temps ?

elif selection == 2:
    #disable camera et llm, reprendre le code au début ?
    #réinitialiser la page et/ou afficher les stats de la session (temps travaillé) : workduration - actualworkduration