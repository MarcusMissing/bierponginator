import os

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from KI import config
from KI.smallervggnet import SmallerVGGNet

# Run Tensorboard: tensorboard --logdir=resource/tensorboard in Terminal

Image_size = config.image_size_gesture
npz_file_path = os.path.join("resource", "preprocessed_images_100.npz")

X_train = np.load(npz_file_path)['X_train']
X_test = np.load(npz_file_path)['X_test']
y_train = np.array(np.load(npz_file_path)['y_train'], dtype='int')
y_test = np.array(np.load(npz_file_path)['y_test'], dtype='int')

# construct the image generator for data augmentation
aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode='nearest')

# initialize the model using a sigmoid activation as the final layer
# in the network so we can perform multi-label classification
model = SmallerVGGNet.build(
    width=Image_size[1], height=Image_size[0],
    depth=Image_size[2], classes=10,
    finalAct='sigmoid')

# model = models.MobileNetv2(input_shape=config.image_size_0, k=10)

# initialize the optimizer (SGD is sufficient)
opt = Adam(lr=config.iteration_learn_rate, decay=config.iteration_learn_rate / config.epochs)

checkpoints_filepath = os.path.join("resource", "checkpoints", "model_100_1.h5")
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoints_filepath,
    save_weights_only=False,
    monitor='accuracy',
    mode='max',
    save_best_only=True)

tensorboard_filepath = os.path.join("resource", "tensorboard")
tensorboard_callback = TensorBoard(log_dir=tensorboard_filepath, histogram_freq=1)
if os.path.exists(os.path.join("resource", "tensorboard", "train")):
    try:
        os.remove(os.path.join("resource", "tensorboard", "train"))
        os.remove(os.path.join("resource", "tensorboard", "validation"))
        print("removed" + str(tensorboard_filepath))
    except Exception as e:
        print(e)

reduce_lr = ReduceLROnPlateau(monitor="binary_crossentropy", factor=0.2, patience=6, min_lr=0.0001)

# compile the model using binary cross-entropy rather than
# categorical cross-entropy -- this may seem counterintuitive for
# multi-label classification, but keep in mind that the goal here
# is to treat each output label as an independent Bernoulli
# distribution
model.compile(loss='binary_crossentropy', optimizer=opt,
              metrics=['accuracy'])

model.fit_generator(
    aug.flow(X_train, y_train, batch_size=config.batch_size),
    validation_data=(X_test, y_test),
    steps_per_epoch=len(X_train) // config.batch_size,
    epochs=config.epochs, verbose=1, callbacks=[model_checkpoint_callback, tensorboard_callback])

# model.save('../resource/model.h5')