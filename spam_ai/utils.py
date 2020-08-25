import pandas as pd
import numpy as np

from tensorflow.keras import models, layers, activations, optimizers, losses, callbacks
from sklearn.model_selection import train_test_split, KFold
import matplotlib.pyplot as plt
import time


class DataModule:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.ARC_path = "ARC.npz"
        self.APP_path = "APP.npz"

    def reading_csv(self):
        csv_reader = pd.read_csv(
            self.csv_path
        )
        label_list = list(csv_reader["v1"])
        data_list = list(csv_reader["v2"])

        np.savez_compressed(self.ARC_path, label=label_list, data=data_list)

    def preprocessing(self, ARC_file):
        nploader = np.load(ARC_file)
        data_list = nploader["data"]
        label_list = nploader["label"]
        new_label_list = list()
        for label in label_list:
            if label == "ham":
                new_label_list.append(0)
            elif label == "spam":
                new_label_list.append(1)

        np.savez_compressed(self.APP_path, data=data_list, label=new_label_list)


class TrainModule:
    def __init__(self, result_name, vocab_size, output_dim, input_length, ckpt_path, model_name):
        self.result_name = result_name
        self.model = models.Sequential([])
        self.input_dim = vocab_size
        self.output_dim = output_dim
        self.input_length = input_length
        self.ckpt_path = ckpt_path
        self.model_name = model_name

    def BuildModel(self):
        self.model = models.Sequential([
            layers.Embedding(
                input_dim=self.input_dim,
                output_dim=self.output_dim,
                input_length=self.input_length
            ),
            layers.Bidirectional(layers.LSTM(128)),
            layers.Dense(128, activation=activations.relu),
            layers.BatchNormalization(),
            layers.Dense(64, activation=activations.relu),
            layers.BatchNormalization(),
            layers.Dense(32, activation=activations.relu),
            layers.Dropout(rate=0.5),
            layers.Dense(2, activation=activations.softmax)
        ])

        self.model.compile(
            optimizer=optimizers.Adam(),
            loss=losses.categorical_crossentropy,
            metrics=["acc"]
        )

        return self.model

    def TrainModel(self, model, x_data, y_data):
        fhandler = open(f"{self.result_name}.txt", 'w')
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1)
        print(np.shape(x_train), np.shape(x_test), np.shape(y_train), np.shape(y_test))

        kf = KFold()
        fold_no = 1
        valid_acc = list()
        valid_loss = list()
        test_acc = list()
        test_loss = list()

        start_time = time.time()
        for train, valid in kf.split(x_train, y_train):
            hist = self.model.fit(
                x=x_train[train], y=y_train[train],
                batch_size=128,
                epochs=1000,
                callbacks=[
                    callbacks.EarlyStopping(
                        min_delta=5e-4,
                        patience=20,
                        verbose=1
                    ),
                    callbacks.ReduceLROnPlateau(
                        factor=0.6,
                        patience=5,
                        verbose=1,
                        min_delta=5e-4,
                        min_lr=1e-6
                    ),
                    callbacks.ModelCheckpoint(
                        filepath=self.ckpt_path,
                        verbose=1,
                        save_best_only=True,
                        save_weights_only=True
                    )
                ],
                validation_data=(x_train[valid], y_train[valid])
            )

            model.load_weights(filepath=self.ckpt_path)
            model.save(filepath=f"{self.model_name}_{fold_no}.h5")

            self.training_visualization(hist=hist.history, fold_no=fold_no)

            fhandler.write(f"\nTraining time for fold {fold_no}: {time.time() - start_time} sec\n")
            valid_score = model.evaluate(x=x_train[valid], y=y_train[valid], verbose=0)
            fhandler.write(
                f"> Validation score for fold {fold_no}: \n"
                f"Score for validation dataset: {model.metrics_names[0]} - {valid_score[0]}; {model.metrics_names[1]} - {valid_score[1] * 100}%"
            )

            test_score = model.evaluate(x=x_test, y=y_test)
            print(
                f"Score for {fold_no} - test set: {model.metrics_names[0]} of {test_score[0]}; {model.metrics_names[1]} of {test_score[1] * 100}%"
            )
            fhandler.write(
                f"\nScore for test set: {model.metrics_names[0]} of {test_score[0]}; {model.metrics_names[1]} of {test_score[1] * 100}%\n"
            )
            fhandler.write("\n--------------------------------------------------------------------------------------\n")

            valid_loss.append(valid_score[0])
            valid_acc.append(valid_score[1] * 100)
            test_loss.append(test_score[0])
            test_acc.append(test_score[1] * 100)

            fold_no += 1

        fhandler.write("\nAverage valid scores for all folds:\n")
        fhandler.write(f"> Accuracy: {np.mean(valid_acc)}% (+- {np.std(valid_acc)})\n")
        fhandler.write(f"> Loss: {np.mean(valid_loss)} (+- {np.std(valid_loss)})\n")

        fhandler.write("\n\nAverage test scores for all folds:\n")
        fhandler.write(f"> Accuracy: {np.mean(test_acc)}% (+- {np.std(test_acc)})\n")
        fhandler.write(f"> Loss: {np.mean(test_loss)} (+- {np.std(test_loss)})\n")

        fhandler.close()

    def training_visualization(self, hist, fold_no):
        localtime = time.localtime()
        tst = str(localtime[0]) + "_" + str(localtime[1]) + "_" + str(localtime[2]) + "_" + str(
            localtime[3]) + "_" + str(localtime[4]) + "_" + str(localtime[5])

        plt.subplot(2, 1, 1)
        plt.plot(hist['acc'], 'b')
        plt.plot(hist['val_acc'], 'g')
        plt.ylim([0, 1])
        plt.xlabel("Epoch")
        plt.ylabel("Accuracies")
        plt.tight_layout()

        plt.subplot(2, 1, 2)
        plt.plot(hist['loss'], 'b')
        plt.plot(hist['val_loss'], 'g')
        plt.ylim([0, 5])
        plt.xlabel("Epoch")
        plt.ylabel("Losses")
        plt.tight_layout()

        fig_path = "fig/" + tst + "_" + str(
            fold_no) + f"_{self.result_name}.png"
        plt.savefig(fname=fig_path, dpi=300)
        plt.clf()
