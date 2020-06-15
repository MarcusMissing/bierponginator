import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

model = load_model('../../resource/model.h5')
X = np.load('../../resource/preprocessed_images_128.npz')['X']

loaded_image = X.__getitem__(500)  # insert number of test image here!
image = img_to_array(loaded_image)
image = np.expand_dims(image, axis=0)

proba = model.predict(image)

for i, j in enumerate(proba[0]):
    print(f'{i}: {round(j * 100, 2)}%')

cv2.imshow('image', loaded_image)
cv2.waitKey(0)
