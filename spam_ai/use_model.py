from tensorflow.keras import models
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle


def is_spam(user_input):
    user_input = np.expand_dims(user_input, axis=0)
    MODEL_PATH = "C:/Users/admin/Documents/Git_public/AI Hackathon/spam_ai/model/spam_ham_2.h5"
    model = models.load_model(MODEL_PATH)

    with open("C:/Users/admin/Documents/Git_public/AI Hackathon/spam_ai/tokenizer.pickle", "rb") as handler:
        tokenizer = pickle.load(handler)

    tokenizer.fit_on_texts(user_input)
    seq = tokenizer.texts_to_sequences(user_input)

    pad = pad_sequences(
        seq,
        maxlen=120,
        padding="post",
        truncating="post"
    )

    results = model.predict(
        x=pad,
        verbose=1
    )
    print(np.argmax(results))
    if np.argmax(results) == 0:
        print("스팸이 아닙니다.")
        return False

    elif np.argmax(results) == 1:
        print("스팸입니다.")
        return True
