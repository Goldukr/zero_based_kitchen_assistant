import tensorflow as tf
from tensorflow.keras import layers, models
import pathlib
import json

# Dataset paths
train_dir = pathlib.Path("data/food_images/train")
val_dir = pathlib.Path("data/food_images/validation")
test_dir = pathlib.Path("data/food_images/test")

IMG_SIZE = (128,128)
BATCH_SIZE = 32

# Load datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    val_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    test_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Save class names (important for prediction)
class_names = train_ds.class_names
print("Classes:", class_names)

with open("models/class_names.json", "w") as f:
    json.dump(class_names, f)

# Improve performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# Data Augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1),
])

# Load MobileNetV2
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128,128,3),
    include_top=False,
    weights="imagenet"
)

# Freeze base model first
base_model.trainable = False

# Build model
model = models.Sequential([
    tf.keras.Input(shape=(128,128,3)),
    data_augmentation,
    layers.Lambda(tf.keras.applications.mobilenet_v2.preprocess_input),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(len(class_names), activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Initial training
model.fit(train_ds, validation_data=val_ds, epochs=15)

# Fine-tuning (unfreeze top layers)
base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(train_ds, validation_data=val_ds, epochs=5)

# Evaluate
test_loss, test_acc = model.evaluate(test_ds)
print("Test Accuracy:", test_acc)

# Save model
model.save("models/food_model.h5")
print("Model saved successfully!")
