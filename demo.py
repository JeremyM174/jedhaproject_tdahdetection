import opencv

def get_emotion_from_image(image: np.ndarray) -> Literal('emotion1', 'emotion2'):
    #IN LOCAL; model is defined earlier
    #model=CNN(...)
    #model.load_state_dict()
    return

def get_message_from_emotion(emotion: str):
    return

for frame in opencv.capture():
    preprocessed_image = preprocess(frame)
    emotion = get_emotion_from_image(preprocessed_image)
    message_to_display_to_user = 
