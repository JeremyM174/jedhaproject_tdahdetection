# **WAKEE : Work Assistant with Kindness & Emotional Empathy 🧠🤗**

### 🚀 Introduction
Bienvenue sur WAKEE (Work Assistant with Kindness & Emotional Empathy), votre assistant de travail intelligent conçu pour améliorer votre concentration et votre bien-être. Ce projet utilise la reconnaissance des émotions par un modèle de réseau de neurones convolutionnel (CNN : EfficientNetB4 fine tuné) combinée aux recommandations personnalisées d'un grand modèle linguistique (LLM : Mistral Small Latest) pour vous offrir un environnement de travail adapté, particulièrement utile pour les personnes atteintes de TDAH.

WAKEE vous aide à rester engagé et productif en détectant vos émotions (ennui, engagement, confusion, frustration) et en vous proposant des suggestions proactives pour vous aider à surmonter les défis et à maintenir votre attention.

### ✨ Fonctionnalités
- Reconnaissance d'Émotions en Temps Réel : Utilisation de votre caméra pour détecter des émotions clés telles que l'ennui, l'engagement, la confusion et la frustration grâce à un réseau de neurones convolutif (CNN).

- Recommandations Personnalisées par LLM : Un grand modèle linguistique analyse les émotions détectées et génère des conseils et des stratégies adaptés pour vous aider à retrouver votre concentration ou à gérer votre état émotionnel.

- Gestion du Temps de Travail : Choisissez une durée de session de travail personnalisée et suivez votre progression grâce à une barre de temps visuelle.

- Interface Intuitive Streamlit : Une interface utilisateur claire et interactive, facilitant l'activation de la caméra, la visualisation des analyses en temps réel et la réception des suggestions.

Conçu pour le Bien-être : Une approche axée sur l'empathie pour créer un environnement de travail plus serein et productif.

🛠️ Installation
Pour faire fonctionner WAKEE sur votre machine locale, suivez ces étapes :

- Cloner le dépôt :
```bash
git clone https://github.com/JeremyM174/jedhaproject_tdahdetection
cd jedhaproject_tdahdetection
```

- Créer un environnement virtuel (recommandé) :
```bash
python -m venv venv
# Sur Windows
.\venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate
```

- Installer les dépendances :
```bash
pip install -r requirements.txt
```

- Configurer sa Clé API (LLM) :
Créer un fichier .env à la racine du projet avec votre clé API.
Exemple de fichier .env :

```bash
MISTRAL_API_KEY="votre_cle_api_mistral"
```
Vous pouvez vous même créer votre clé API Mistral : [https://admin.mistral.ai/organization/api-keys]


### 🚀 Utilisation
Pour démarrer l'application Streamlit :

```Bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut.

### 💡 Comment ça Marche ?
- Choisissez votre temps de travail : Utilisez le curseur pour définir la durée de votre session.

- Activez votre caméra : Cliquez sur le bouton "Activer ma caméra".

- Suivez votre progression : Une barre de progression vous montrera le temps écoulé.

- Recevez des suggestions de Wakee : L'assistant analysera vos expressions et vous proposera des recommandations contextuelles pour vous aider à rester concentré et positif.

### Datasets

* **DAiSEE (Dataset for Affective States in E-Learning Environments)**
    * **Auteurs :**
        * Deepak S. Rajpoot
        * Tania Das
        * N. G. Gadge
        * Mayank Nag
        * Abhishek Kumar
        * Alok Kumar
    * **Source / Lien :** [https://daisee.org/](https://daisee.org/)
    * **Description :** Le dataset DAiSEE contient des vidéos d'étudiants en train de suivre des tutoriels en ligne, annotées pour quatre états affectifs (Ennui, Engagement, Frustration, Confusion) ainsi que le niveau d'engagement. Il a été utilisé dans ce projet pour [expliquer brièvement comment vous l'avez utilisé, ex: "l'entraînement d'un modèle de reconnaissance de l'engagement émotionnel"]. Nous avons récupéré une version plus légère du dataset sous format photos sur Kaggle [https://www.kaggle.com/datasets/johnykletka12348/daiseecvproject]
    * **Référence académique (si vous voulez être très précis) :** Si vous avez trouvé une publication scientifique associée au dataset (souvent disponible sur le site du dataset ou via Google Scholar), vous pouvez ajouter une citation dans un format académique commun (par exemple, APA, IEEE, etc.), ou simplement le titre et la conférence/journal. Par exemple :
        > Rajpoot, D. S., Das, T., Gadge, N. G., Nag, M., Kumar, A., & Kumar, A. (2018). *DAiSEE: Towards VAE-LSTM based Emotion Recognition in E-Learning Environments*. (À compléter avec la conférence/journal exacte si vous la trouvez, ex: "Proceedings of the IEEE International Conference on Automatic Face & Gesture Recognition (FG)").

### 📞 Contact
Albert ROMANO - [https://github.com/Ter0rra]
Asma RHALMI - [https://github.com/Cauliflaa]
Jeremy MARIARGE - [https://github.com/JeremyM174]
Manon FAEDY - [https://github.com/ManonFAEDY]