import tensorflow as tf
from KI import config

resnet = tf.keras.applications.ResNet50V2(
    include_top=False,
    weights="imagenet",
    input_tensor=None,
    input_shape=config.image_size_gesture,
    pooling="max",
)
for layer in resnet.layers[0:-3]:
    layer.trainable = False

model_layer = tf.keras.layers.Flatten()(resnet.output)
model_layer = tf.keras.layers.Dense(512)(model_layer)
model_layer = tf.keras.layers.Dropout(0.5)(model_layer)
model_layer = tf.keras.layers.Dense(512)(model_layer)
model_layer = tf.keras.layers.Dropout(0.5)(model_layer)
model_layer = tf.keras.layers.Dense(128)(model_layer)
model_layer = tf.keras.layers.Dropout(0.5)(model_layer)
output = tf.keras.layers.Dense(3)(model_layer)
model = tf.keras.Model(inputs=resnet.inputs, outputs=output)
model.summary()