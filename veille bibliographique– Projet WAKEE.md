# 📚 Références & Crédits – Projet WAKEE

Ce document regroupe toutes les **références scientifiques, techniques et crédits** utilisés pour le développement de **WAKEE**, une application locale de détection d’émotions et d’aide à la concentration.

---

## 📊 Dataset principal : DAiSEE

Le projet WAKEE s'appuie principalement sur le dataset **DAiSEE** (*Dataset for Affective States in E-learning Environments*), conçu pour analyser l'engagement des utilisateurs dans un contexte d’apprentissage en ligne.

### 🧾 Détails du dataset :
- **Créateurs** : Gupta, D’Cunha, Awasthi, Balasubramanian (Indian Institute of Technology Hyderabad)
- **Participants** : 112 individus filmés en conditions réelles
- **Volume** : 9 068 vidéos (~25 heures de données)
- **Étiquettes émotionnelles** : 
  - 4 émotions : Engagement, Ennui (Boredom), Confusion, Frustration
  - 4 niveaux d’intensité : Very Low, Low, High, Very High
  - Validation par des psychologues et annotations crowdsourcées

### 📁 Lien vers le dataset :
- Arxiv : https://arxiv.org/abs/1609.01885
- Kaggle : https://www.kaggle.com/datasets/olgaparfenova/daisee

### 📖 Référence complète (APA) :
Gupta, A., D’Cunha, A., Awasthi, K., & Balasubramanian, V. (2016). *DAiSEE: Towards User Engagement Recognition in the Wild*. arXiv preprint arXiv:1609.01885.

---

## 🧠 Références scientifiques complémentaires

WAKEE s’appuie également sur des travaux académiques de référence dans la détection des émotions et l’engagement :

1. **Zeng, Z., Pantic, M., Roisman, G.I., & Huang, T.S. (2009).**
   *A Survey of Affect Recognition Methods: Audio, Visual, and Spontaneous Expressions.* IEEE Transactions on Pattern Analysis and Machine Intelligence, 31(1), 39–58.

2. **Bosch, N., D’Mello, S., & Ocumpaugh, J. (2015).**
   *Detecting student emotions in computer-enabled classrooms.* International Journal of Artificial Intelligence in Education, 25(2), 158–190.

---

## ⚙️ Technologies & bibliothèques utilisées

WAKEE a été développé en **Python 3.11.13** avec un ensemble de bibliothèques spécialisées :

- **OpenCV** – pour la capture vidéo et le traitement d’image
- **CNN (Convolutional Neural Network)** – pour analyser les images et détecter les émotions
- **LLM (Large Language Model)** – pour générer des messages empathiques
- **numpy==1.26.4** – calculs numériques et manipulation des données
- **opencv-python==4.7.0.72** – interface Python pour OpenCV
- **dotenv** – gestion des variables d’environnement
- **pillow** – traitement d’images
- **onnxruntime** – exécution des modèles CNN optimisés
- **torchvision** – outils pour la vision par ordinateur et les CNN
- **langchain_core** – structure pour la gestion du LLM
- **langchain_mistralai** – intégration avec le modèle Mistral

---

## 🙏 Crédits & Remerciements

Un grand merci :  
- Aux chercheurs de l’**Indian Institute of Technology Hyderabad** pour la création du dataset **DAiSEE**.  
- À **Olga Parfenova** pour la mise à disposition des données sur Kaggle.  
- Aux contributeurs des bibliothèques **OpenCV**, **PyTorch**, **LangChain** et autres outils open source utilisés.  
- Aux encadrants et formateurs de **Jedha Bootcamp** pour leur accompagnement et leurs conseils.

---

📌 Ce document constitue la **référence bibliographique et technique officielle** du projet WAKEE.
