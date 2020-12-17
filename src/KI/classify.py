import os
import pickle
import socket
import struct
import sys
import time

import cv2
import numpy as np
from tensorflow.keras.models import load_model

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


def local_classify(model, model_gestures, fps):
    while True:
        cap = cv2.VideoCapture(0)

        img_full = cap.read()[1]
        time.sleep(fps)

        score_gestures, score = live_classify(img_full, model, model_gestures)

        score_gestures_indice = np.argmax(score_gestures, axis=1)
        gestures = ["Thumbs up", "O-Finger", "Peace"]
        if score_gestures[0, score_gestures_indice] > config.gesture_treshhold:
            gesture = gestures[int(score_gestures_indice)]
        else:
            gesture = "-----"

        img_big = cv2.resize(img_full, (1000, 1000))
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(img_big, "current NN input resolution: " + str(config.image_size_gesture), (40, 80), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "Gesture: " + gesture, (40, 950), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, str(np.round(score_gestures[0, :], 3)), (300, 950), font, 0.8,
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


def init_conn():
    host = ''
    port = 9999

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((host, port))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn, addr = s.accept()
    print("Connection established")
    return conn


def remote_classify(conn, model, model_gestures):
    data = b""
    payload_size = struct.calcsize(">L")
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        img_full = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        img_full = cv2.imdecode(img_full, cv2.IMREAD_COLOR)

        score_gestures, score = live_classify(img_full, model, model_gestures)
        data_string = [[]]
        data_string[0] = np.round(score[0, 0:])

        score_gestures_indice = np.argmax(score_gestures, axis=1)
        gestures = ["Thumbs up", "O-Finger", "Peace"]
        if score_gestures[0, score_gestures_indice] > config.gesture_treshhold:
            gesture = gestures[int(score_gestures_indice)]
        else:
            gesture = "-----"

        data_string.append(gesture)
        data_string = pickle.dumps(data_string, 0)
        conn.send(data_string)


def live_classify(img_full, model, model_gestures):
    temp_gesture = np.empty((1, *config.image_size_gesture))
    temp_pong = np.empty((1, *config.image_size_pong))

    temp_pong[0, :] = cv2.resize(img_full, config.image_size_pong[0:2])
    temp_pong = np.divide(temp_pong, 255)
    score = model.predict(temp_pong)

    temp_gesture[0, :] = cv2.resize(img_full, config.image_size_gesture[0:2])
    temp_gesture = np.divide(temp_gesture, 255)
    score_gestures = model_gestures.predict(temp_gesture)

    return score_gestures, score


if __name__ == '__main__':
    model_path = os.path.join("..", "..", "resource", "checkpoints", "model_100_1.h5")
    model = load_model(model_path)
    model_path_gestures = os.path.join("..", "..", "resource", "checkpoints", "model_gestures_200_1.h5")
    model_gestures = load_model(model_path_gestures)
    # classify(model)
    if sys.argv[1] == "local":
        local_classify(model, model_gestures, fps=0)
    elif sys.argv[1] == "remote":
        remote_classify(init_conn(), model, model_gestures)
