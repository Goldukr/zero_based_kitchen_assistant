'''import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import pathlib
import os
import json


# Load trained model
model = tf.keras.models.load_model("models/food_model.h5")

# Get class names automatically from train folder
train_dir = pathlib.Path("data/food_images/train")
class_names = sorted([item.name for item in train_dir.iterdir() if item.is_dir()])
with open("models/class_names.json") as f:
    class_names = json.load(f)

print("Classes:", class_names)

# Image path
image_path = "data/food_images/test/apple/Image_1.jpg"   # put test image in project folder

# Load and preprocess image
img = Image.open(image_path).convert("RGB").resize((128,128))
img_array = np.array(img)   # no /255
img_array = np.expand_dims(img_array, axis=0)

#predict 
prediction = model.predict(img_array)
predicted_index = np.argmax(prediction)
predicted_item = class_names[predicted_index]

print("Predicted Food:", predicted_item)


# Load shelf life file
shelf_file = "shelf_life.csv"

if os.path.exists(shelf_file):
    shelf_df = pd.read_csv(shelf_file)
    row = shelf_df[shelf_df["item"] == predicted_item]
    
    if not row.empty:
        expiry_days = int(row["days"].values[0])
    else:
        expiry_days = 5   # default expiry
else:
    expiry_days = 5

# Add to inventory
inventory_file = "inventory.csv"

new_data = {
    "item": predicted_item,
    "added_date": datetime.today().strftime("%Y-%m-%d"),
    "expiry_days": expiry_days
}

if os.path.exists(inventory_file):
    df = pd.read_csv(inventory_file)
    df = df._append(new_data, ignore_index=True)
else:
    df = pd.DataFrame([new_data])

df.to_csv(inventory_file, index=False)
prediction = model.predict(img_array)
predicted_class = np.argmax(prediction)

print("Probabilities:", prediction[0])
print("Classes:", class_names)


print("Item added to inventory successfully!")
'''


import json
import numpy as np
from PIL import Image
import tensorflow as tf

image_path = "data/food_images/test/apple/Image_1.jpg"  # update as needed

model = tf.keras.models.load_model(
    "models/food_model.h5",
    custom_objects={
        "preprocess_input": tf.keras.applications.mobilenet_v2.preprocess_input
    },
)

# Load class names
with open("models/class_names.json") as f:
    class_names = json.load(f)

img = Image.open(image_path).convert("RGB").resize((128,128))
img_array = np.array(img)
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)
predicted_item = class_names[np.argmax(prediction)]

print("Predicted Food:", predicted_item)

