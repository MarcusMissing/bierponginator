from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
from KI import config

paths = []
paths.extend([str(p) for p in Path("resource/images/images_labeled").rglob("*" + ".jpg")])
X = np.empty((len(paths) * 3, *config.image_size_0))
y = np.zeros((len(paths)*3, 10))

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

    y_label = ID.split(".")[0]
    y_label = y_label[-10:]
    for k in range(10):
        y[j, k] = np.array(y_label[k], dtype="float64")
        y[j + len(paths), k] = np.array(y_label[k], dtype="float64")
        y[j + len(paths) * 2, k] = np.array(y_label[k], dtype="float64")

# ---------------- save as npz ----------------
np.savez_compressed('resource/preprocessed_images_128_new.npz', y=y, X=X)
