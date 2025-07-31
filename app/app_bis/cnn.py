import onnxruntime as ort
import numpy as np
import torchvision.transforms.v2 as transforms

# Variable globale pour stocker la session
_session = None

def _load_model():
    """Charge le modèle ONNX une seule fois"""
    global _session
    if _session is None:
        try:
            _session = ort.InferenceSession("daisee_model.onnx")
            # print("✅ Modèle ONNX chargé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle : {e}")
            raise
    return _session

def get_emotion(pil_image):

    # # Charger le modèle ONNX
    # session = ort.InferenceSession("daisee_model.onnx")

     # Charger le modèle si pas déjà fait (lazy loading)
    session = _load_model()

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                            [0.229, 0.224, 0.225])
    ])

    input_tensor = transform(pil_image).unsqueeze(0).numpy()  # (1, 3, 224, 224)

    # Faire une prédiction
    outputs = session.run(['output'], {'input': input_tensor})
    preds = outputs[0]
    

    return preds