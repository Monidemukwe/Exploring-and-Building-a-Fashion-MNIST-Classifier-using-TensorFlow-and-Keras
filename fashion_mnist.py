# -*- coding: utf-8 -*-
"""fashion-mnist.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17p6LPvcLopK9E7KNd7o6G_ELLwNdr4if

# <a id="2">Load packages</a>
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import tensorflow as tf
from tensorflow import keras
from keras.utils import plot_model

import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

"""## Parameters"""

# Dataset params
IMG_ROWS = 28
IMG_COLS = 28
NUM_CLASSES = 10
TEST_SIZE = 0.2
RANDOM_STATE = 2024

#Model params
NUMB_EPOCHS = 50
BATCH_SIZE = 128

"""* Each row is a separate image
* Column 1 is the class label(the article of clothing).
* Remaining columns are pixel numbers (784 total).
* Each value is the darkness of the pixel (1 to 255)

"""

train = pd.read_csv("fashion-mnist_train.csv")
test = pd.read_csv("fashion-mnist_test.csv")

train.shape

type(train)

"""### From Keras

Keras provides some utility functions to fetch and load common datasets, including Fashion MNIST. One important difference is that every image is represented as a 28×28 array rather than a 1D array of size 784.

"""

(X_train_full, y_train_full), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

X_train_full.shape

type(X_train_full)

"""It's a numpy array rather than a Pandas DataFrame.

# <a id="4">Data exploration</a>
"""

train.head()

print("Fashion MNIST train shape -->", train.shape)
print("Fashion MNIST test shape  -->", train.shape)

"""## <a id="41">Classes distribution</a>

Let's see how many number of images are in each class for the train set and test set
"""

train["label"].value_counts()

test["label"].value_counts()

f, ax = plt.subplots(1,2, figsize=(12,4))
g1 = sns.countplot(data=train, x='label', ax=ax[0])
g2 = sns.countplot(data=test, x='label', ax=ax[1])

g1.set_title("Classes Distribution in the Train set")
g2.set_title("Classes Distribution in the Test set")
plt.show()

"""In the train and the test set the 10 classes are equaly distributed (10% each).

## <a id="42">Sample images</a>

### Train set images

Let's plot some samples for the images.   
We add labels to the train set images, with the corresponding fashion item category.
"""

# dictionary for each type of label
labels = {0 : "T-shirt/top", 1: "Trouser", 2: "Pullover", 3: "Dress", 4: "Coat",
          5: "Sandal", 6: "Shirt", 7: "Sneaker", 8: "Bag", 9: "Ankle Boot"}

def sample_images_data(data):
    # An empty list to collect some samples
    sample_images = []
    sample_labels = []

    # Iterate over the keys of the labels dictionary defined in the above cell
    for k in labels.keys():
        # Get four samples for each category
        samples = data[data["label"] == k].head(4)
        # Append the samples to the samples list
        for j, s in enumerate(samples.values):
            # First column contain labels, hence index should start from 1
            img = np.array(samples.iloc[j, 1:]).reshape(28, 28)
            sample_images.append(img)
            sample_labels.append(samples.iloc[j, 0])

    print("Total number of sample images to plot: ", len(sample_images))
    return sample_images, sample_labels

train_sample_images, train_sample_labels = sample_images_data(train)

"""Let's now plot the images.   
The labels are shown above each image.
"""

def plot_sample_images(data_sample_images,data_sample_labels,cmap="Blues"):
    # Plot the sample images now
    f, ax = plt.subplots(5,8, figsize=(16,10))

    for i, img in enumerate(data_sample_images):
        ax[i//8, i%8].imshow(img, cmap=cmap)
        ax[i//8, i%8].axis('off')
        ax[i//8, i%8].set_title(labels[data_sample_labels[i]])
    plt.show()

plot_sample_images(train_sample_images,train_sample_labels, "Greens")

"""### Test set images

Let's plot now a selection of the test set images.  
Labels are as well added (they are known).  
"""

test_sample_images, test_sample_labels = sample_images_data(test)
plot_sample_images(test_sample_images,test_sample_labels)

"""# <a id="5">Model</a>

We start with preparing the model.

## <a id="51">Prepare the model</a>

### Data preprocessing

First we will do a data preprocessing to prepare for the model.

Since the second dataset is already a numpy matrix (28,28,1) and has been splitted to train aand test, we'll use it. We must create a validation set and scale the input features so since we are going to train the neural network using Gradient Descent.   
For simplicity, we'll just scale the pixel intensities down to the 0-1 range by dividing them by 255.0.
"""

X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=[28, 28]))
model.add(tf.keras.layers.Dense(300, activation='relu'))
model.add(tf.keras.layers.Dense(100, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

"""### Inspect the model

The model’s summary() method displays all the model’s layers, including each layer’s name (which is automatically generated unless you set it when creating the layer), its
output shape (None means the batch size can be anything), and its number of parameters. The summary ends with the total number of parameters, including trainable and non-trainable parameters.
"""

model.summary()

"""Let's also plot the model"""

plot_model(model, to_file='model.png')

"""We can easily get a model’s list of layers, to fetch a layer by its index, or you can fetch it by name"""

model.layers

model.compile(loss="sparse_categorical_crossentropy",
             optimizer="sgd",
             metrics=["accuracy"])

"""### Training and Evaluating the Model

Now the model is ready to be trained. For this we simply need to call its fit() method on the training set. We are also using the validation set (a subset from the orginal training set) for validation.
"""

history = model.fit(X_train, y_train,
                  epochs=30,
                  validation_data=(X_valid, y_valid))

"""## <a id="53">Test prediction accuracy</a>

We calculate the test loss and accuracy.
"""

model.evaluate(X_test, y_test)

"""Test accuracy is  around  0.84.

We evaluated the model accuracy based on the predicted values for the test set.  Let's check the validation value during training.

## <a id="54">Validation accuracy and loss</a>

Let's plot the train and validation accuracy and loss, from the train history.
"""

pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1) # set the vertical range to [0-1]
plt.show()

"""Both the training and validation accuracy steadily increase during training, while the training and validation loss decrease. Good! Moreover, the validation curves are quite close to the training curves, which means that there is not too much overfitting."""