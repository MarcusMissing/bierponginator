from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
from KI import config
import random
import os

paths = []
img_path = os.path.join("resource", "images", "gestures")
paths.extend([str(p) for p in Path(img_path).rglob("*" + ".png")])
paths.extend([str(p) for p in Path(img_path).rglob("*" + ".jpg")])

X = np.empty((len(paths) , *config.image_size_gesture))
y = np.zeros((len(paths)))
random.seed = 49
random.shuffle(paths)

for j, ID in tqdm(enumerate(paths)):
    try:
        img_full = cv2.imread(ID)
        img = cv2.resize(img_full, config.image_size_gesture[0:2])
        img = np.divide(img, 255)
    except Exception as e:
        print(e)
        img = np.zeros(config.image_size_gesture)
    X[j,] = img
    y[j] = int(ID.split(".")[-3])


# ---------------- save as npz ----------------
train_split = len(X) - int(config.train_test_split * len(X))
file_name = "preprocessed_images_gestures" + str(config.image_size_gesture[0])
npz_path = os.path.join("resource", "images", "compressed", file_name)
np.savez_compressed(npz_path, y_train=y[0:train_split],
                    y_test=y[train_split + 1:len(X)], X_train=X[0:train_split],
                    X_test=X[train_split + 1:len(X)])
