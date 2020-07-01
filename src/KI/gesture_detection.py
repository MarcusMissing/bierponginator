import cv2
import numpy as np
import time
import os
import cv2
from pathlib import Path
from tqdm import tqdm


def capture_img(frames_per_gesture: int, gestures: int, resolution: tuple = (100, 100)):
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        time.sleep(5)
        print("---------------------------START -------------------------------------------------")
        for i in range(gestures):
            for j in range(frames_per_gesture):
                ret, img = cap.read()
                time.sleep(0.1)
                filename = "gesture." + str(i) + "." + str(j + 300) + ".png"
                img_name = os.path.join("resource", "images", "gestures", filename)
                cv2.imwrite(img_name, img)
                cv2.imshow('camera output', img)
                k = cv2.waitKey(10)
                if k == 48:
                    break
                if j % 10 == 0:
                    print("---------------------------Change something----------------------------------------")
                    time.sleep(2)
            print("###################################################################################")
            print("#########################  Change Gesture  ########################################")
            print("###################################################################################")

        break


def clean_scraped_imgs():
    dataset = os.path.join("..", "..", "resource", "images", "scraped_gestures", "thumbsup")
    paths = []
    paths.extend([str(p) for p in Path(dataset).rglob("*" + ".jpg")])
    for i, path in tqdm(enumerate(paths)):
        img_full = cv2.imread(path)
        if img_full is None:
            os.remove(path)
            print("removed: " + str(path))
            continue
        if img_full.shape[0] < 200 or img_full.shape[1] < 200:
            os.remove(path)
            print("removed: " + str(path))
            continue
        img = cv2.resize(img_full, (400, 400))
        img_name = path[0:-4].split(os.sep)[-1]
        img_name = img_name.replace(".", "")
        img_name = os.path.join("..", "..", "resource", "images", "scraped_gestures", "thumbsup",
                                "gesture_scraped." + str(0) + "." + img_name + ".jpg")
        cv2.imwrite(img_name, img)
        os.remove(path)


if __name__ == '__main__':
    # capture_img(frames_per_gesture=200, gestures=4)
    clean_scraped_imgs()
