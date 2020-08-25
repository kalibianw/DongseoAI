from tensorflow.keras.utils import to_categorical
import numpy as np


nploader = np.load("APP.npz")

for key in nploader:
    print(key)

data_array, label_array = nploader["data"], nploader["label"]
label_array = to_categorical(label_array)

print(np.shape(data_array), np.shape(label_array))
print(label_array)
