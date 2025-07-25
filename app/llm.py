from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI
import random

chaleureux = """Tu es une IA empathique conçue pour accompagner les adultes atteints de TDAH pendant leur travail.
Lorsque tu détectes une émotion négative, tu donnes un petit message rassurant et motivant.
Ton style est chaleureux, court (1-2 phrases), facile à lire et à comprendre.
Varie ta formulation à chaque fois pour éviter les répétitions."""

reconfortant = """Tu es une petite voix intérieure pour les personnes atteintes de TDAH.
Quand une émotion apparaît, tu proposes une phrase brève qui aide à se recentrer, respirer ou se reconnecter à la tâche.
Garde un ton doux, réconfortant, et varie tes messages pour éviter la lassitude.
Tu n’écris jamais plus de 2 phrases."""

energique = """Tu es une IA énergique et bienveillante. Ton objectif est de booster la concentration de personnes atteintes de TDAH.
Tu détectes une émotion et tu balances une phrase courte, motivante, jamais la même.
Tu peux être drôle, douce, ou sérieuse, mais toujours utile.
Pas plus de 20 mots."""

positif = """Tu es un assistant IA formé à la psychologie positive pour personnes avec TDAH.
Quand une émotion est détectée, tu réponds par un message court, valorisant et encourageant.
Ton style est clair, bienveillant, et chaque message est unique.
Tu aides à retrouver confiance, calme ou focus avec 1-2 phrases maximum."""

liste_system_templates = [chaleureux, reconfortant, energique, positif]



boredom = "L’utilisateur semble s’ennuyer : produis une seule phrase d’encouragement pour l’aider à retrouver de l’intérêt dans sa tâche."

engagement = "L’utilisateur paraît concentré et engagé : produis une seule phrase de félicitations pour renforcer sa motivation et son focus."

disengagement = "L’utilisateur semble perdre de l’intérêt ou se détourner de sa tâche : produis une phrase courte et encourageante pour l’aider à se recentrer et retrouver sa motivation."

confusion = "L’utilisateur semble confus : produis une seule phrase simple et claire pour l’aider à clarifier sa pensée et se recentrer."

frustration = "L’utilisateur semble frustré : produis une seule phrase de soutien pour l’aider à lâcher prise et retrouver son calme."

incertitude = "Une émotion semble présente, mais elle n’est pas clairement identifiable : propose une phrase courte, neutre et rassurante qui aide l’utilisateur à rester calme et concentré."

liste_user_templates = [boredom, engagement, disengagement, confusion, frustration, incertitude]



def match_emotion_response(emotion):
    emotions = {"boredom" : boredom, "engagement" : engagement, "disengagement" : disengagement, "confusion" : confusion, "frustration" : frustration, "incertitude" : incertitude}
    if emotion in emotions:
        return emotions[emotion]
    else:
        raise ValueError("Unexpected prediction received from CNN")
    


def get_recommendation(emotion):

    system_template = random.choice(liste_system_templates)
    prompt_template = ChatPromptTemplate.from_messages([
        ('system', system_template),
        ('user', '{text}')
    ])

    model = ChatMistralAI(model="mistral-small-latest")
    parser = StrOutputParser()

    pipe_sequence = (
        prompt_template
        .pipe(model)
        .pipe(parser)
    )

    response = (pipe_sequence.invoke({
        "émotion": emotion,
        "text": match_emotion_response(emotion)
    }))

    return response