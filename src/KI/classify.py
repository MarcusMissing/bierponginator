import os
import time
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from KI import config


def classify(model):
    npz_file_path = os.path.join("resource", "preprocessed_images_100.npz")
    X_test = np.load(npz_file_path)['X_test']
    y_test = np.array(np.load(npz_file_path)['y_test'], dtype='int')
    # proba = model.predict(X_test)
    score = model.predict(X_test)
    print(score)
    for i, j in enumerate(score):
        print(f'{i}:\n {np.round(j)}')
        print(y_test[i])
        img = cv2.resize(X_test[i,], (500, 500))
        cv2.imshow('image', img)
        cv2.waitKey(0)


def live_classify(model, fps):
    cap = cv2.VideoCapture(0)
    temp = np.zeros((1, *config.image_size_0))
    while (cap.isOpened()):
        img_full = cap.read()[1]
        time.sleep(fps)
        img = cv2.resize(img_full, config.image_size_0[0:2])
        temp[0, :] = img
        score = model.predict(temp)
        img_big = cv2.resize(img_full, (1000,1000))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_big, str(np.round(score,2)), (20, 950), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "current NN input resolution: " + str(config.image_size_0), (40, 80), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "Press 0 to terminate", (40, 40), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('camera output', img_big)
        k = cv2.waitKey(10)
        if k == 48:
            break
        print(score)


if __name__ == '__main__':
    model_path = os.path.join("resource", "checkpoints", "model_100_1.h5")
    model = load_model(model_path)
    opt = Adam(lr=config.iteration_learn_rate, decay=config.iteration_learn_rate / config.epochs)
    model.compile(loss='binary_crossentropy', optimizer=opt,
                  metrics=['accuracy'])
    # classify(model)
    live_classify(model, fps=0)
