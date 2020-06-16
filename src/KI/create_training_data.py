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
X = np.empty((len(paths) * 3, *config.image_size_0))
y = np.zeros((len(paths) * 3))
random.seed = 49
random.shuffle(paths)

for j, ID in tqdm(enumerate(paths)):
    img_full = cv2.imread(ID)
    img = cv2.resize(img_full, config.image_size_0[0:2])
    img = np.divide(img, 255)
    X[j + len(paths) * 2,] = img

    rand_length = img_full.shape[1] // np.random.randint(6, 10)
    if np.random.rand(1) < 0.5:
        img_crop = img_full[rand_length:, rand_length:]
    else:
        img_crop = img_full[:img.shape[0] - rand_length, :img.shape[1] - rand_length]
    img_crop = cv2.resize(img_crop, config.image_size_0[0:2])
    img_crop = np.divide(img_crop, 255)
    X[j,] = img_crop
    row, col, ch = img.shape
    mean = 0.5
    var = 0.01
    sigma = var ** 5
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    gauss = gauss.reshape(row, col, ch)
    img_gauss = img + gauss
    X[j + len(paths),] = img_gauss

    y_label = ID.split(".")[-3]
    #y_label = y_label[-10:]
    #for k in range(10):
    y[j] = np.array(y_label, dtype="int")
    y[j + len(paths)] = np.array(y_label, dtype="int")
    y[j + len(paths) * 2] = np.array(y_label, dtype="int")

# ---------------- save as npz ----------------
train_split = len(X) - int(config.train_test_split * len(X))
file_name = "preprocessed_images_gestures" + str(config.image_size_0[0])
npz_path = os.path.join("resource", "images", "compressed", file_name)
np.savez_compressed(npz_path, y_train=y[0:train_split],
                    y_test=y[train_split + 1:len(X)], X_train=X[0:train_split],
                    X_test=X[train_split + 1:len(X)])
