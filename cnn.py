import onnxruntime as ort
import numpy as np
import torchvision.transforms.v2 as transforms

def get_emotion(pil_image):

    # Charger le modèle ONNX
    session = ort.InferenceSession(r"C:\Users\maria\Desktop\dsfs_ft_35\00_Projets_certif\bloc6_lead-data-project_finalproject\jedhaproject_tdahdetection\daisee_model.onnx")

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