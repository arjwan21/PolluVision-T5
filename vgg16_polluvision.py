# -*- coding: utf-8 -*-
"""VGG16_PolluVision (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BS6qIDhJm1S_WUKr-a5wb-XWk6UlsoNL
"""

# connect to drive
from google.colab import drive
drive.mount('/content/drive')

"""#1. Import Required Libraries"""

#import required libraries — we do need the models, flatten, dense, input layers
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential

"""#2. Import the Dataset from Roboflow Website"""

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="wBhhcFexJ3QDDrx6zu0d")
project = rf.workspace("sdaia-xqoon").project("capstone-avmph")
dataset = project.version(8).download("tensorflow")

"""# 3. Change the Annotations of Train, Validation, and test sets

## 3.1. Change Train Annotations
"""

import pandas as pd
df = pd.read_csv('/content/Capstone-8/train/_annotations.csv')
# Rename the class column to label
df.rename(columns={'class':'label'},inplace = True)
# Drop the Width, Hight columns from the annotation
df.drop(['width','height'],axis=1,inplace=True)
df.head()

# Save train annotation
df.to_csv('/content/Capstone-8/train/_annotations.csv',index=False)

import os
import cv2
import pandas as pd
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import to_categorical

# Path to the folder containing the images
image_folder = '/content/Capstone-8/train/'

# Path to the CSV file
csv_file = '/content/Capstone-8/train/_annotations.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Create a dictionary to map string labels to integer labels
label_mapping_train = {label: index for index, label in enumerate(df['label'].unique())}

# Prepare the inputs and labels for training
train_images = []
train_labels = []

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    image_name = row['filename']
    label = row['label']
    xmin = row['xmin']
    ymin = row['ymin']
    xmax = row['xmax']
    ymax = row['ymax']

    # Construct the image path
    image_path = os.path.join(image_folder, image_name)

    # Read and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
     # Append the preprocessed image and label to the training data
    train_images.append(img)
    train_labels.append(label_mapping_train[label])

# Convert the training data to numpy arrays
train_images = np.array(train_images)
train_labels = np.array(train_labels)

# Convert labels to one-hot encoded format
train_labels = to_categorical(train_labels)

"""### 3.1.1. Normalize Train Data"""

images_train = []
for filename in df['filename']:
    img_path = os.path.join(image_folder, filename)
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = img / 255.0  # normalize pixel values
    images_train.append(img)

train_images = np.array(images_train)

"""## 3.2. Change Valid Annotations"""

import pandas as pd
df = pd.read_csv('/content/Capstone-8/valid/_annotations.csv')
# Rename the class column to label
df.rename(columns={'class':'label'},inplace = True)
# Drop the Width, Hight columns from the annotation
df.drop(['width','height'],axis=1,inplace=True)
df.head()

# Save valid annotation
df.to_csv('/content/Capstone-8/valid/_annotations.csv',index=False)

import os
import cv2
import pandas as pd
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import to_categorical

# Path to the folder containing the images
image_folder = '/content/Capstone-8/valid/'

# Path to the CSV file
csv_file = '/content/Capstone-8/valid/_annotations.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Create a dictionary to map string labels to integer labels
label_mapping_valid = {label: index for index, label in enumerate(df['label'].unique())}

# Prepare the inputs and labels for training
valid_images = []
valid_labels = []

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    image_name = row['filename']
    label = row['label']
    xmin = row['xmin']
    ymin = row['ymin']
    xmax = row['xmax']
    ymax = row['ymax']

    # Construct the image path
    image_path = os.path.join(image_folder, image_name)

    # Read and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
     # Append the preprocessed image and label to the training data
    valid_images.append(img)
    valid_labels.append(label_mapping_valid[label])

# Convert the training data to numpy arrays
valid_images = np.array(valid_images)
valid_labels = np.array(valid_labels)

# Convert labels to one-hot encoded format
valid_labels = to_categorical(valid_labels)

"""### 3.2.1. Normalize Valid Data"""

images_valid = []
for filename in df['filename']:
    img_path = os.path.join(image_folder, filename)
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = img / 255.0  # normalize pixel values
    images_valid.append(img)

valid_images = np.array(images_valid)

"""## 3.3. Change Test Annotations"""

import pandas as pd
df = pd.read_csv('/content/Capstone-8/test/_annotations.csv')
# Rename the class column to label
df.rename(columns={'class':'label'},inplace = True)
# Drop the Width, Hight columns from the annotation
df.drop(['width','height'],axis=1,inplace=True)
df.head()

# Save test annotation
df.to_csv('/content/Capstone-8/test/_annotations.csv',index=False)

import os
import cv2
import pandas as pd
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import to_categorical

# Path to the folder containing the images
image_folder = '/content/Capstone-8/test/'

# Path to the CSV file
csv_file = '/content/Capstone-8/test/_annotations.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Create a dictionary to map string labels to integer labels
label_mapping_test = {label: index for index, label in enumerate(df['label'].unique())}

# Prepare the inputs and labels for training
test_images = []
test_labels = []

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    image_name = row['filename']
    label = row['label']
    xmin = row['xmin']
    ymin = row['ymin']
    xmax = row['xmax']
    ymax = row['ymax']

    # Construct the image path
    image_path = os.path.join(image_folder, image_name)

    # Read and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
     # Append the preprocessed image and label to the training data
    test_images.append(img)
    test_labels.append(label_mapping_test[label])

# Convert the training data to numpy arrays
test_images = np.array(test_images)
test_labels = np.array(test_labels)

# Convert labels to one-hot encoded format
test_labels = to_categorical(test_labels)

"""### 3.3.1. Normalize Test Data"""

images_test = []
for filename in df['filename']:
    img_path = os.path.join(image_folder, filename)
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = img / 255.0  # normalize pixel values
    images_test.append(img)

test_images = np.array(images_test)

"""# 4. Download VGG16 model"""

# Create a VGG16 model, and removing the last layer that is classifying 1000 images. This will be replaced with images classes we have.
IMAGE_SIZE = [224, 224]
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False) #Training with Imagenet weights
vgg.trainable = False ## Not trainable weights

vgg.summary()

"""##4.1. Modify the Model Layers"""

from tensorflow.keras.layers import Conv2D
# Add our layers
# This sets the base that the layers are not trainable. If we'd want to train the layers with custom data, these two lines can be ommitted.
for layer in vgg.layers:
  layer.trainable = False

x = Conv2D(70, (1, 1), activation='relu')(vgg.output)
f1 = Flatten()(x) #Output obtained on vgg16 is now flattened.
d2 = Dense(70, activation='relu')(f1)
prediction = Dense(9, activation='softmax')(d2) # We have 5 classes, and so, the prediction is being done on len(folders) - 5 classes
#Creating model object
model = Model(inputs=vgg.input, outputs=prediction)
model.summary()

"""## 4.1.1. Draw the Model Architecture

"""

!pip install pydot

from tensorflow.keras.utils import plot_model

plot_model(model, show_shapes=True, show_layer_names=True)

"""## 4.2. Train the Model"""

from tensorflow.keras.callbacks import EarlyStopping

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define early stopping callback
es = EarlyStopping(monitor='val_accuracy', mode='max', patience=5, restore_best_weights=True)

# Train the model
history = model.fit(train_images, train_labels , validation_data=(valid_images, valid_labels ), epochs=50, batch_size=64, callbacks=[es])

print(label_mapping_test)

"""# 5. Predict & Visulize some images"""

import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

# Path to the image file
image_path = '/content/Capstone-8/test/04c74fb6ff31ac072c204d468ae5b7de_jpg.rf.b6bb903aa921d203fa2bf713b24c6c8c.jpg'

label_mapping_tests = {
    0: 'garbage',
    1: 'construction_waste',
    2: 'graffiti',
    3: 'sand_on_road',
    4: 'construction_road',
    5: 'potholes',
    6: 'bad_billboard',
    7: 'clutter_sidewalk',
    8: 'broken_signage',
}
# Load and preprocess the image
img = image.load_img(image_path, target_size=(224, 224))
img = image.img_to_array(img)
img = preprocess_input(img)

# Reshape the image to match the model's input shape
img = np.expand_dims(img, axis=0)

# Make predictions on the image using the trained model
predictions = model.predict(img)
# Get the predicted label and bounding box coordinates
predicted_label = np.argmax(predictions, axis=1)[0]
bounding_box = predictions[0, 1:]  # Assuming the 0th index corresponds to the background class

# Create a dictionary to map integer labels back to their respective string labels
label_mapping_inverse = {index: label for label, index in label_mapping_tests.items()}

# Read the image
img = cv2.imread(image_path)

# Get the image dimensions
height, width, _ = img.shape

# Extract the bounding box coordinates
xmin = int(bounding_box[0] * width)
ymin = int(bounding_box[1] * height)
xmax = int(bounding_box[2] * width)
ymax = int(bounding_box[3] * height)

# Draw the bounding box on the image
cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

# Get the predicted label
predicted_label = label_mapping_inverse.get(predicted_label, "Unknown label")

# Add the predicted label text to the image
label_text = f"Label: {predicted_label}"
cv2.putText(img, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with bounding box and predicted label using matplotlib
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

# Path to the image file
image_path ='/content/Capstone-8/test/3518d589fbf05f96e35a59630f5eb594_jpg.rf.b89b80c3ac3a2ce42c4d7f3877622f94.jpg'

label_mapping_tests = {
    0: 'garbage',
    1: 'construction_waste',
    2: 'graffiti',
    3: 'sand_on_road',
    4: 'construction_road',
    5: 'potholes',
    6: 'bad_billboard',
    7: 'clutter_sidewalk',
    8: 'broken_signage',
}
# Load and preprocess the image
img = image.load_img(image_path, target_size=(224, 224))
img = image.img_to_array(img)
img = preprocess_input(img)

# Reshape the image to match the model's input shape
img = np.expand_dims(img, axis=0)

# Make predictions on the image using the trained model
predictions = model.predict(img)
# Get the predicted label and bounding box coordinates
predicted_label = np.argmax(predictions, axis=1)[0]
bounding_box = predictions[0, 1:]  # Assuming the 0th index corresponds to the background class

# Create a dictionary to map integer labels back to their respective string labels
label_mapping_inverse = {index: label for label, index in label_mapping_tests.items()}

# Read the image
img = cv2.imread(image_path)

# Get the image dimensions
height, width, _ = img.shape

# Extract the bounding box coordinates
xmin = int(bounding_box[0] * width)
ymin = int(bounding_box[1] * height)
xmax = int(bounding_box[2] * width)
ymax = int(bounding_box[3] * height)

# Draw the bounding box on the image
cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

# Get the predicted label
predicted_label = label_mapping_inverse.get(predicted_label, "Unknown label")

# Add the predicted label text to the image
label_text = f"Label: {predicted_label}"
cv2.putText(img, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with bounding box and predicted label using matplotlib
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

# Path to the image file
image_path ='/content/Capstone-8/test/59c381218eee247398087a0d8a5052cd_jpg.rf.380437fca6e565a662bd072e0359ec6d.jpg'

label_mapping_tests = {
    0: 'garbage',
    1: 'construction_waste',
    2: 'graffiti',
    3: 'sand_on_road',
    4: 'construction_road',
    5: 'potholes',
    6: 'bad_billboard',
    7: 'clutter_sidewalk',
    8: 'broken_signage',
}
# Load and preprocess the image
img = image.load_img(image_path, target_size=(224, 224))
img = image.img_to_array(img)
img = preprocess_input(img)

# Reshape the image to match the model's input shape
img = np.expand_dims(img, axis=0)

# Make predictions on the image using the trained model
predictions = model.predict(img)
# Get the predicted label and bounding box coordinates
predicted_label = np.argmax(predictions, axis=1)[0]
bounding_box = predictions[0, 1:]  # Assuming the 0th index corresponds to the background class

# Create a dictionary to map integer labels back to their respective string labels
label_mapping_inverse = {index: label for label, index in label_mapping_tests.items()}

# Read the image
img = cv2.imread(image_path)

# Get the image dimensions
height, width, _ = img.shape

# Extract the bounding box coordinates
xmin = int(bounding_box[0] * width)
ymin = int(bounding_box[1] * height)
xmax = int(bounding_box[2] * width)
ymax = int(bounding_box[3] * height)

# Draw the bounding box on the image
cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

# Get the predicted label
predicted_label = label_mapping_inverse.get(predicted_label, "Unknown label")

# Add the predicted label text to the image
label_text = f"Label: {predicted_label}"
cv2.putText(img, label_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Display the image with bounding box and predicted label using matplotlib
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

