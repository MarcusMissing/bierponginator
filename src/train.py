import numpy as np
import tensorflow as tf

import model_base, config

if __name__ == '__main__':
    image_size = config.image_size_0
    batch_size = config.batch_size
    epochs = config.epochs

    checkpoint_filepath = 'resource/tmp/checkpoint'
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_filepath,
        save_weights_only=False,
        monitor='categorical_accuracy',
        mode='max',
        save_best_only=True)

    # model = MobileNetv2(input_shape=config.image_size_0, k=10)
    model = model_base.model
    model.summary()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["categorical_accuracy"]
    )
    X = np.load("resource/preprocessed_images.npz")['X']
    y = np.array(np.load("resource/preprocessed_images.npz")["lables"], dtype="int")
    model.fit(
        X, y, epochs=config.epochs, callbacks=[model_checkpoint_callback], validation_split=0.05,
        batch_size=config.batch_size
    )
