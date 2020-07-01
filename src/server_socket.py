import os
import pickle
import socket
import struct
import time

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from KI import config

HOST = ''
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

model_path = os.path.join("..", "resource", "checkpoints", "model_100_1.h5")
model = load_model(model_path)
model_path_gestures = os.path.join("..", "resource", "checkpoints", "model_gestures_100_1.h5")
model_gestures = load_model(model_path_gestures)
opt = Adam(lr=config.iteration_learn_rate, decay=config.iteration_learn_rate / config.epochs)
model.compile(loss='binary_crossentropy', optimizer=opt,
              metrics=['accuracy'])


def live_classify(model, model_gestures, fps):
    data = b""
    payload_size = struct.calcsize(">L")

    temp = np.zeros((1, *config.image_size))
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

        time.sleep(fps)
        img = cv2.resize(img_full, config.image_size[0:2])
        temp[0, :] = img
        score = model.predict(temp)
        score_gestures = model_gestures.predict(temp)
        score_gestures_max = np.argmax(score_gestures)
        if score_gestures_max == 0:
            gesture = "Thumbs up"
        if score_gestures_max == 1:
            gesture = "Ciao Bella"
        if score_gestures_max == 2:
            gesture = "Peace"
        if score_gestures_max == 3:
            gesture = "Nothing"

        img_big = cv2.resize(img_full, (1000, 1000))
        font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(img_big, str(np.round(score, 2)), (20, 950), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "current NN input resolution: " + str(config.image_size), (40, 80), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, "Gesture: " + gesture, (40, 950), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, str(np.round(score_gestures, 2)), (300, 950), font, 0.8,
                    (0, 255, 0), 2, cv2.LINE_AA)

        pred_str_1 = "    [" + str(np.round(score[0, 0], 2)) + "]"
        pred_str_2 = "   " + str(np.round(score[0, 1:3], 2))
        pred_str_3 = " " + str(np.round(score[0, 3:6], 2))
        pred_str_4 = "" + str(np.round(score[0, 6:], 2))

        cv2.putText(img_big, pred_str_1, (700, 800), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, pred_str_2, (700, 850), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, pred_str_3, (700, 900), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img_big, pred_str_4, (700, 950), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        data_string = pickle.dumps(score, 0)
        conn.send(data_string)

        cv2.putText(img_big, "Press 0 to terminate", (40, 40), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        #cv2.imshow('camera output', img_big)
        k = cv2.waitKey(10)
        if k == 48:
            break


if __name__ == '__main__':
    live_classify(model, model_gestures, fps=0)
