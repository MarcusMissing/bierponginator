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


def live_classify(model, model_gestures, fps):
    cap = cv2.VideoCapture(0)
    temp_gesture = np.zeros((1, *config.image_size_gesture))
    temp_pong = np.zeros((1, *config.image_size_pong))

    while (cap.isOpened()):
        img_full = cap.read()[1]
        time.sleep(fps)
        img_gesture = cv2.resize(img_full, config.image_size_gesture[0:2])
        img_pong = cv2.resize(img_full, config.image_size_pong[0:2])
        temp_pong[0, :] = img_pong
        score = model.predict(temp_pong)
        temp_gesture[0, :] = img_gesture
        score_gestures = model_gestures.predict(temp_gesture)
        score_gestures_indice = np.argmax(score_gestures, axis=1)
        gestures = ["Thumbs up", "O-Fingeronis", "Peace"]
        if len(np.where(score_gestures == 1.0)[1]) > 1:
            gesture = "unsure"
        elif score_gestures[0, score_gestures_indice] > config.gesture_treshhold:
            gesture = gestures[int(score_gestures_indice)]
        else:
            gesture = "-----"

        img_big = cv2.resize(img_full, (1000, 1000))
        font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(img_big, str(np.round(score, 2)), (20, 950), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "current NN input resolution: " + str(config.image_size_gesture), (40, 80), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "Gesture: " + gesture, (40, 950), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, str(np.round(score_gestures[0, :], decimals=3)), (300, 950), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)

        pred_str_1 = "    [" + str(np.round(score[0, 0], 2)) + "]"
        pred_str_2 = "   " + str(np.round(score[0, 1:3], 2))
        pred_str_3 = " " + str(np.round(score[0, 3:6], 2))
        pred_str_4 = "" + str(np.round(score[0, 6:], 2))

        cv2.putText(img_big, pred_str_4, (700, 800), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, pred_str_3, (700, 850), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, pred_str_2, (700, 900), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, pred_str_1, (700, 950), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(img_big, "Press 0 to terminate", (40, 40), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('camera output', img_big)
        k = cv2.waitKey(10)
        if k == 48:
            break
        print(score)


if __name__ == '__main__':
    model_path = os.path.join("resource", "checkpoints", "model_100_1.h5")
    model = load_model(model_path)
    model_path_gestures = os.path.join("resource", "checkpoints", "model_gestures_140_1.h5")
    model_gestures = load_model(model_path_gestures)
    opt = Adam(lr=config.iteration_learn_rate, decay=config.iteration_learn_rate / config.epochs)
    model.compile(loss='binary_crossentropy', optimizer=opt,
                  metrics=['accuracy'])
    # classify(model)
    live_classify(model, model_gestures, fps=0)
