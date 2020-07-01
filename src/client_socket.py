import pickle
import socket
import struct

import cv2


def start_classify():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('Gaming-PC', 9999))

    cam = cv2.VideoCapture(0)

    cam.set(3, 320)
    cam.set(4, 240)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while True:
        frame = cam.read()[1]
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        client_socket.sendall(struct.pack(">L", size) + data)

        score = client_socket.recv(1024)
        score = pickle.loads(score)
        print(score)

    cam.release()
