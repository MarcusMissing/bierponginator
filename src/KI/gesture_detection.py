import cv2
import numpy as np
import time
import os
from KI import config


def capture_img(frames_per_gesture: int, gestures: int, resolution: tuple = (100, 100)):
    X = np.zeros((frames_per_gesture * gestures, *resolution, 3))
    y = np.zeros((frames_per_gesture * gestures, 1))

    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        time.sleep(5)
        print("---------------------------START -------------------------------------------------")
        for i in range(gestures):
            for j in range(frames_per_gesture):
                ret, img = cap.read()
                # X[j + frames_per_gesture * i,:] = np.array(cv2.resize(img, resolution))
                # y[j + frames_per_gesture * i,:] = i
                time.sleep(0.8)
                filename = "gesture." + str(i) + "." + str(j+200) + ".png"
                img_name = os.path.join("resource", "images", "gestures", filename)
                cv2.imwrite(img_name, img)
                cv2.imshow('camera output', img)
                k = cv2.waitKey(10)
                if k == 48:
                    break
                if j % 10 == 0:
                    print("---------------------------Change something----------------------------------------")
                    time.sleep(3)
            print("###################################################################################")
            print("---------------------------Change Gesture------------------------------------------")
            print("###################################################################################")

        # filename = "gestures_" + str(resolution) + ".npz"
        # npz_file_path = os.path.join("resource", "images", "compressed", filename)
        # train_split = len(X) - int(0.05 * len(X))
        # np.savez_compressed(npz_file_path, y_train=y[0:train_split],
        #                     y_test=y[train_split + 1:len(X)], X_train=X[0:train_split,],
        #                     X_test=X[train_split + 1:len(X)],)
        break


if __name__ == '__main__':
    capture_img(frames_per_gesture=100, gestures=4)
