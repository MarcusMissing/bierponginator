import os

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

from KI import config

model_path = os.path.join("resource", "checkpoints", "model_100_1.h5")
model = load_model(model_path)

opt = Adam(lr=config.iteration_learn_rate, decay=config.iteration_learn_rate / config.epochs)
model.compile(loss='binary_crossentropy', optimizer=opt,
              metrics=['accuracy'])

# loaded_image = X.__getitem__(500)  # insert number of test image here!
# image = img_to_array(loaded_image)
# image = np.expand_dims(image, axis=0)

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

