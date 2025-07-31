
# **WAKEE: Work Assistant with Kindness & Emotional Empathy 🧠🤗**

### 🚀 Introduction
Welcome to WAKEE (Work Assistant with Kindness & Emotional Empathy), your intelligent work assistant designed to improve your focus and well-being. This project leverages emotion recognition through a Convolutional Neural Network model (CNN: fine-tuned EfficientNetB4) combined with personalized recommendations from a Large Language Model (LLM: Mistral Small Latest) to offer a tailored work environment, particularly useful for people with ADHD.

WAKEE helps you stay engaged and productive by detecting your emotions (boredom, engagement, confusion, frustration) and offering proactive suggestions to help you overcome challenges and maintain focus.

### ✨ Features
- **Real-Time Emotion Recognition:** Uses your camera to detect key emotions such as boredom, engagement, confusion, and frustration via a convolutional neural network (CNN).

- **Personalized Recommendations via LLM:** A large language model analyzes the detected emotions and generates tips and strategies to help you regain focus or manage your emotional state.

- **Work Session Management:** Set a custom work session duration and track your progress with a visual time bar.

- **Streamlit User Interface:** A clear, interactive interface to enable the camera, view real-time analyses, and receive suggestions.

- **Focus on Well-being:** An empathy-driven approach to create a calmer, more productive work environment.

### 🛠️ Installation
To run WAKEE locally, follow these steps:

- Clone the repository:
```bash
git clone https://github.com/JeremyM174/jedhaproject_tdahdetection
cd jedhaproject_tdahdetection
```

- Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
.env\Scriptsctivate
# On macOS/Linux
source venv/bin/activate
```

- Install dependencies:
```bash
pip install -r requirements.txt
```

- Configure your API key (LLM):
Create a `.env` file at the root of the project with your API key.
Example:
```bash
MISTRAL_API_KEY="your_mistral_api_key"
```
You can create your own Mistral API key: [https://admin.mistral.ai/organization/api-keys]

### 🚀 Usage
To start the Streamlit application:
```bash
streamlit run app.py
```

The application will open automatically in your default browser.

### 💡 How It Works?
- **Choose your work session time:** Use the slider to set the session duration.
- **Activate your camera:** Click on the “Activate my camera” button.
- **Track your progress:** A progress bar will show elapsed time.
- **Receive suggestions from WAKEE:** The assistant will analyze your expressions and propose contextual recommendations to help you stay focused and positive.


### 📞 Contact
- Albert ROMANO - [https://github.com/Ter0rra]
- Asma RHALMI - [https://github.com/Cauliflaa]
- Jeremy MARIARGE - [https://github.com/JeremyM174]
- Manon FAEDY - [https://github.com/ManonFAEDY]

---

## 📊 Dataset & Bibliography

WAKEE is primarily based on the **DAiSEE dataset** (*Dataset for Affective States in E-Learning Environments*), designed to analyze user engagement in online learning contexts.

### 🧾 Dataset Details
- **Creators:** Gupta, D’Cunha, Awasthi, Balasubramanian (Indian Institute of Technology Hyderabad)  
- **Participants:** 112 individuals filmed in real conditions  
- **Volume:** 9,068 videos (~25 hours of data)  
- **Emotions:** Engagement, Boredom, Confusion, Frustration (4 intensity levels: Very Low, Low, High, Very High)  
- **Validation:** Labels confirmed by psychologists and crowdsourcing.  
- **Links:**  
  - [Arxiv Publication](https://arxiv.org/abs/1609.01885)  
  - [Kaggle Dataset](https://www.kaggle.com/datasets/olgaparfenova/daisee)  

📖 **APA Reference:** Gupta, A., D’Cunha, A., Awasthi, K., & Balasubramanian, V. (2016). *DAiSEE: Towards User Engagement Recognition in the Wild*. arXiv preprint arXiv:1609.01885.

---

### 🧠 Additional Scientific References
1. **Zeng, Z., Pantic, M., Roisman, G.I., & Huang, T.S. (2009).**  
   *A Survey of Affect Recognition Methods: Audio, Visual, and Spontaneous Expressions.* IEEE TPAMI.

2. **Bosch, N., D’Mello, S., & Ocumpaugh, J. (2015).**  
   *Detecting student emotions in computer-enabled classrooms.* International Journal of AI in Education.


---

## ⚙️ Technologies & Libraries Used

WAKEE was developed in **Python 3.11.13** with the following key libraries:

- **OpenCV** – video capture and image processing
- **CNN (Convolutional Neural Network)** – to analyze images and detect emotions
- **LLM (Large Language Model)** – to generate empathic messages
- **numpy==1.26.4** – numerical computations and data manipulation
- **opencv-python==4.7.0.72** – Python interface for OpenCV
- **dotenv** – environment variable management
- **pillow** – image processing
- **onnxruntime** – optimized CNN model execution
- **torchvision** – computer vision and CNN tools
- **langchain_core** – framework for LLM integration
- **langchain_mistralai** – integration with the Mistral model
- **Streamlit** – web interface for real-time app 

---

## 🙏 Credits & Acknowledgments

A big thank you to:
- The researchers at the **Indian Institute of Technology Hyderabad** for creating the **DAiSEE** dataset.  
- **Olga Parfenova** for making the dataset available on Kaggle.  
- The contributors of **OpenCV**, **PyTorch**, **LangChain**, and other open-source tools used.  
- The instructors and mentors of the **Jedha Bootcamp** for their support and guidance.

---

📌 This document serves as the **official bibliographic and technical reference** for the WAKEE project.
