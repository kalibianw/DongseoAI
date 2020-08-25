from spam_ai.utils import DataModule
import numpy as np


dm = DataModule(
    csv_path="spam.csv"
)

user_input = int(input(
    "1. Reading_csv\n"
    "2. Preprocessing (reading_csv required)\n"
    "3. Checking ARC.npz\n"
    "4. Checking APP.npz"
))

if user_input == 1:
    dm.reading_csv()

elif user_input == 2:
    dm.preprocessing("ARC.npz")

elif user_input == 3:
    nploader = np.load("ARC.npz")
    label_list = nploader["label"]
    data_list = nploader["data"]

    for label in label_list:
        print(label)
        print(type(label))
    for data in data_list:
        print(data)
        print(type(data))

elif user_input == 4:
    nploader = np.load("APP.npz")
    new_label_list = nploader["label"]
    data_list = nploader["data"]

    for label in new_label_list:
        print(label)
        print(type(label))
    for data in data_list:
        print(data)
        print(type(data))

