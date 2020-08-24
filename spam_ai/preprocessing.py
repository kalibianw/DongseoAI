from spam_aI_model.utils import DataModule
import numpy as np


dm = DataModule(
    csv_path="spam.csv"
)

user_input = int(input(
    "1. reading_csv\n"
    "2. preprocessing (reading_csv required)\n"
    "3. "
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
