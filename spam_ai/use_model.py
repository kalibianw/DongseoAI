from tensorflow.keras import models
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import sys
import os


os.system("cls")

model = models.load_model("model/spam_ham_2.h5")

user_input = sys.argv[1]
print("----------------------------------------------------------------------")
print(user_input)
print("----------------------------------------------------------------------")

tokenizer = Tokenizer(
    num_words=1000,
    oov_token="<OOV>"
)
tokenizer.fit_on_texts(user_input)
seq = tokenizer.texts_to_sequences(user_input)

pad = pad_sequences(
    seq,
    maxlen=120,
    padding="post",
    truncating="post"
)
print(f"shape of pad: {np.shape(pad)}")


result = model.predict(
    x=pad,
    verbose=1
)

print(result)
print(f"shape of result: {np.shape(result)}")
print(np.argmax(result))
print(np.max(result))
