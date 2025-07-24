import onnxruntime as ort
import numpy as np
import torchvision.transforms.v2 as transforms
#from PIL import Image

def cnn(pil_image):
    #list of emotion
    EMOTION_LABELS = ['Disconnection','Doubt/Confusion','Fatigue','Pain','Disquietment','Annoyance','others','adhd_emotion']

    # Charger le modèle ONNX
    session = ort.InferenceSession("emotic_model.onnx")

    # Charger et prétraiter une image
    # image = pil_image.convert('RGB')
    # image = Image.open(pil_image).convert("RGB")

    transform = transforms.Compose([
        transforms.RGB(),
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
    # Transformer la pred en list 
    list_of_pred = preds[0].tolist()
    # Find the first emotion without adhd_emotion
    emotion = list_of_pred[0:-1].index(max(list_of_pred[0:-1]))
    # get the result 
    result = EMOTION_LABELS[emotion]
    # print le result 
    # print(result)

    return result