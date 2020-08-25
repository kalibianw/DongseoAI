from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

from spam_ai.utils import TrainModule


nploader = np.load("APP.npz")
data = nploader["data"]
label = nploader["label"]

vocab_size = 1000
embedding_dim = 64
max_length = 120
trunc_type = 'post'
padding_type = 'post'
oov_tok = "<OOV>"
training_size = 4000

tm = TrainModule(
    result_name="training_result",
    vocab_size=vocab_size,
    output_dim=embedding_dim,
    input_length=max_length,
    ckpt_path="ckpt/spam_ham.ckpt",
    model_name="model/spam_ham"
)

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(data)
seq = tokenizer.texts_to_sequences(data)
# print(seq)
# print(np.shape(seq))

pad = pad_sequences(
    seq,
    maxlen=max_length,
    padding=padding_type,
    truncating=trunc_type
)
# print(pad)
# print(np.shape(pad))

model = tm.BuildModel()
model.summary()

tm.TrainModel(
    model,
    x_data=pad,
    y_data=label
)

nploader = np.load("APP.npz")
