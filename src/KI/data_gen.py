from pathlib import Path

import cv2
import numpy as np

from KI import config

paths = []
paths.extend([str(p) for p in Path("resource/bilder_labeles").rglob("*" + ".jpg")])
# limited test size
paths = paths[0:2]

for i in range(3):
    if i == 0:
        image_size = config.image_size_0
    elif i == 1:
        image_size = config.image_size_1
    elif i == 1:
        image_size = config.image_size_2

    # ---------------- run 1 ----------------
    X0 = np.empty((len(paths), *image_size))
    y = np.zeros((len(paths), 10))

    for j, ID in enumerate(paths):
        img = cv2.imread(ID)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if np.random.rand(1) < 0.6:
            # print("img cropped")
            rand_length = img.shape[1] // np.random.randint(8, 14)
            if np.random.rand(1) < 0.6:
                img = img[rand_length:, rand_length:]
            else:
                img = img[:img.shape[0] - rand_length, :img.shape[1] - rand_length]
        img = cv2.resize(img, (image_size[0], image_size[1]))
        img = np.divide(img, 255)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        X0[j,] = img
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        y_label = ID.split(".")[0]
        y_label = y_label[-10:]
        for k in range(10):
            y[j, k] = np.array(y_label[k], dtype="float64")

    # ---------------- run 2 ----------------

    X1 = np.empty((len(paths), *image_size))

    for j, ID in enumerate(paths):
        img = cv2.imread(ID)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if np.random.rand(1) < 0.6:
            # print("img cropped")
            rand_length = img.shape[1] // np.random.randint(8, 14)
            if np.random.rand(1) < 0.6:
                img = img[rand_length:, rand_length:]
            else:
                img = img[:img.shape[0] - rand_length, :img.shape[1] - rand_length]
        img = cv2.resize(img, (image_size[0], image_size[1]))
        img = np.divide(img, 255)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        w = img.shape[1]
        h = img.shape[0]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), np.random.choice([90, 180, 270]), 1)
        img = cv2.warpAffine(img, M, (w, h))
        # print("flipped img vertically")
        if np.random.rand(1) < 0.2:
            row, col, ch = img.shape
            mean = 0.5
            var = 0.01
            sigma = var ** 5
            gauss = np.random.normal(mean, sigma, (row, col, ch))
            gauss = gauss.reshape(row, col, ch)
            img = img + gauss
            # print("added noise")
        X1[i,] = img
        # cv2.imshow('image', img)
        # cv2.waitKey(0)

    # ---------------- run 3 ----------------
    X2 = np.empty((len(paths), *image_size))

    for j, ID in enumerate(paths):
        img = cv2.imread(ID)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if np.random.rand(1) < 0.6:
            # print("img cropped")
            rand_length = img.shape[1] // np.random.randint(8, 14)
            if np.random.rand(1) < 0.6:
                img = img[rand_length:, rand_length:]
            else:
                img = img[:img.shape[0] - rand_length, :img.shape[1] - rand_length]
        img = cv2.resize(img, (image_size[0], image_size[1]))
        img = np.divide(img, 255)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if np.random.rand(1) < 0.2:
            w = img.shape[1]
            h = img.shape[0]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), np.random.choice([90, 180, 270]), 1)
            img = cv2.warpAffine(img, M, (w, h))
            # print("flipped img vertically")
        row, col, ch = img.shape
        mean = 0.5
        var = 0.01
        sigma = var ** 5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        img = img + gauss
        # print("added noise")
        X2[i,] = img
        # cv2.imshow('image', img)
        # cv2.waitKey(0)

    if i == 0:
        res128 = [X0, X1, X2]
    elif i == 1:
        res256 = [X0, X1, X2]
    elif i == 1:
        res512 = [X0, X1, X2]


# ---------------- save as npz ----------------
np.savez_compressed('resource/preprcessed_images', lables=y, res128=res128, res256=res256, res512=res512)
