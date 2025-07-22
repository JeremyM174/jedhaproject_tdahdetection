import opencv

def get_emotion_from_image(image: np.ndarray) -> Literal['emotion1', 'emotion2']:
    # model = my_model_for_emotion.Model()
    # model.predict()
    response = requests.post(url, image)
    return

def get_message_from_emotion(emotion: str) -> str:
    return

for frame in opencv.capture():
    preprocessed_image = preprocess(frame)
    emotion = get_emotion_from_image(preprocessed_image)
    message_to_display_to_user = get_message_from_emotion(emotion)
    print(message_to_display_to_user)