from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
from KI import config
import random
import os
from src import RESOURCE_DIR

paths = []
img_path = os.path.join("resource", "images", "gestures")
paths.extend([str(p) for p in Path(img_path).rglob("*" + ".png")])
paths.extend([str(p) for p in Path(img_path).rglob("*" + ".jpg")])

X = np.zeros((len(paths), *config.image_size_gesture))
y = np.zeros((len(paths)))
random.seed = 49
random.shuffle(paths)

for j, ID in tqdm(enumerate(paths)):
    la = ID.split(".")[-3]
    y[j] = int(la)
    if y[j] > 2:
        print("skipped")
        y[j] = 0
        continue

    try:
        img_full = cv2.imread(ID)
        img = cv2.resize(img_full, config.image_size_gesture[0:2])
        img = np.divide(img, 255)
    except Exception as e:
        print(e)
        img = np.zeros(config.image_size_gesture)
    X[j,] = img

# ---------------- save as npz ----------------
train_split = len(X) - int(config.train_test_split * len(X))
file_name = "preprocessed_images_gestures_" + str(config.image_size_gesture[0])
npz_path = os.path.join(RESOURCE_DIR, "compressed", file_name)
np.savez_compressed(npz_path, y=y, X=X)
