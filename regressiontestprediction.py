# -*- coding: utf-8 -*-
"""RegressionTestPrediction.ipynb
#COLLAB Share Link.  Can run all the code here
#https://colab.research.google.com/drive/1HyaVEnjIG0oVk2fHbOUTtY0q74DSJaK-#scrollTo=6SWtkIjhrZwa
Automatically generated by Colaboratory.

Original tutorial is located at
    https://colab.research.google.com/drive/1HyaVEnjIG0oVk2fHbOUTtY0q74DSJaK-

###This Regression program was adapted from a tutorial 
https://www.tensorflow.org/tutorials/keras/regression

# Basic regression: Predict Test Scores
"""

# Use seaborn for pairplot.
!pip install -q seaborn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Make NumPy printouts easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

"""## The Student Performance Data

The dataset is available from the [Provided File StudentsPerformance.csv]

### Get the data
First download and import the dataset using pandas:
"""

url = 'https://raw.githubusercontent.com/ifritt1525/NnetworkProj/main/StudentsPerformance.csv'
column_names = ['Gender', 'Race/Ethnicity', 'Parental Level of Education', 'Lunch', 'Test Prep',
                'Math Score', 'Reading Score', 'Writing Score']

raw_dataset = pd.read_csv(url, names=column_names,
                          na_values='?', comment='\t',
                          sep=',', skipinitialspace=True, skiprows=1)

dataset = raw_dataset.copy()

dataset.dtypes

"""### One Hot Code the data sets

The `"Gender", "Race", "Parental Level Edu", "Lunch", "Test Prep"` columns are categorical, not numeric. So the next step is to one-hot encode the values in the column with [pd.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html).
"""

dataset['Gender'] = dataset['Gender'].map({'female': 'female', 'male': 'male'})
dataset['Race/Ethnicity'] = dataset['Race/Ethnicity'].map({'group A': 'groupA', 'group B': 'groupB', 'group C': 'groupC', 'group D': 'groupD', 'group E': 'groupE'})
dataset['Parental Level of Education'] = dataset['Parental Level of Education'].map({"associate's degree": 'AD', "bachelor's degree": 'BD', 'high school': 'HS', "master's degree": 'MD', 'some college': 'SC', 'some high school': 'SHS'})
dataset['Lunch'] = dataset['Lunch'].map({'free/reduced': 'f/r', 'standard': 'std'})
dataset['Test Prep'] = dataset['Test Prep'].map({'completed': 'Studied', 'none': 'Lazy'})

dataset = pd.get_dummies(dataset, columns=['Gender'], prefix='', prefix_sep='')
dataset = pd.get_dummies(dataset, columns=['Race/Ethnicity'], prefix='', prefix_sep='')
dataset = pd.get_dummies(dataset, columns=['Parental Level of Education'], prefix='', prefix_sep='')
dataset = pd.get_dummies(dataset, columns=['Lunch'], prefix='', prefix_sep='')
dataset = pd.get_dummies(dataset, columns=['Test Prep'], prefix='', prefix_sep='')
dataset.tail()

dataset.dtypes

"""### Split the data into training and test sets

Now, split the dataset into a training set and a test set. You will use the test set in the final evaluation of your models.
"""

train_dataset = dataset.sample(frac=0.75, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

"""### Split features from labels

Separate the target value???the "label"???from the features. This label is the value that you will train the model to predict.
"""

train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels_MATH = train_features.pop('Math Score')
train_labels_WRITING = train_features.pop('Writing Score')
train_labels_READING = train_features.pop('Reading Score')
test_labels_MATH = test_features.pop('Math Score')
test_labels_WRITING = test_features.pop('Writing Score')
test_labels_READING = test_features.pop('Reading Score')

"""### The Normalization layer

The `tf.keras.layers.Normalization` is a clean and simple way to add feature normalization into your model.

The first step is to create the layer:
"""

normalizer = tf.keras.layers.Normalization(axis=-1)

"""Then, fit the state of the preprocessing layer to the data by calling `Normalization.adapt`:"""

normalizer.adapt(np.array(train_features))

"""Calculate the mean and variance, and store them in the layer:"""

print(normalizer.mean.numpy())

"""When the layer is called, it returns the input data, with each feature independently normalized:"""

first = np.array(train_features[:1])

with np.printoptions(precision=2, suppress=True):
  print('First example:', first)
  print()
  print('Normalized:', normalizer(first).numpy())

"""## Linear regression

Before building a deep neural network model, start with linear regression using one and several variables.

### Linear regression with one variable

Begin with a single-variable linear regression to predict `'MATH SCORE'` from `'Studied'`.

Training a model with `tf.keras` typically starts by defining the model architecture. Use a `tf.keras.Sequential` model, which [represents a sequence of steps](.././guide/keras/sequential_model.ipynb).

There are two steps in your single-variable linear regression model:

- Normalize the `'Studied'` input features using the `tf.keras.layers.Normalization` preprocessing layer.
- Apply a linear transformation ($y = mx+b$) to produce 1 output using a linear layer (`tf.keras.layers.Dense`).

The number of _inputs_ can either be set by the `input_shape` argument, or automatically when the model is run for the first time.

First, create a NumPy array made of the `'Studied'` features. Then, instantiate the `tf.keras.layers.Normalization` and fit its state to the `Studied` data:
"""

studyPower = np.array(train_features['Studied'])

studyPower_normalizer = layers.Normalization(input_shape=[1,], axis=None)
studyPower_normalizer.adapt(studyPower)

"""Build the Keras Sequential model:"""

studypower_model_MATH = tf.keras.Sequential([
    studyPower_normalizer,
    layers.Dense(units=1)
])

studypower_model_MATH.summary()

studypower_model_READING = tf.keras.Sequential([
    studyPower_normalizer,
    layers.Dense(units=1)
])

studypower_model_READING.summary()

studypower_model_WRITING = tf.keras.Sequential([
    studyPower_normalizer,
    layers.Dense(units=1)
])

studypower_model_WRITING.summary()

"""This model will predict `'Math Score'` from `'Studied'`.

Run the untrained model on the first 10 'Studied' values. The output won't be good, but notice that it has the expected shape of `(10, 1)`:
"""

studypower_model_MATH.predict(studyPower[:10])
studypower_model_WRITING.predict(studyPower[:10])
studypower_model_READING.predict(studyPower[:10])

"""Once the model is built, configure the training procedure using the Keras `Model.compile` method. The most important arguments to compile are the `loss` and the `optimizer`, since these define what will be optimized (`mean_absolute_error`) and how (using the `tf.keras.optimizers.Adam`)."""

studypower_model_MATH.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

studypower_model_WRITING.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')


studypower_model_READING.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

"""Use Keras `Model.fit` to execute the training for 100 epochs:"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_MATH = studypower_model_MATH.fit(
#     train_features['Studied'],
#     train_labels_MATH,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.25)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_WRITING = studypower_model_WRITING.fit(
#     train_features['Studied'],
#     train_labels_WRITING,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.25)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_READING = studypower_model_READING.fit(
#     train_features['Studied'],
#     train_labels_READING,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.25)

"""Collect the results on the test set for later:"""

test_results = {}

test_results['studypower_model_math'] = studypower_model_MATH.evaluate(
    test_features['Studied'],
    test_labels_MATH, verbose=0)


test_results['studypower_model_writing'] = studypower_model_WRITING.evaluate(
    test_features['Studied'],
    test_labels_WRITING, verbose=0)

test_results['studypower_model_reading'] = studypower_model_READING.evaluate(
    test_features['Studied'],
    test_labels_READING, verbose=0)

"""### Linear regression with multiple inputs

You can use an almost identical setup to make predictions based on multiple inputs. This model still does the same $y = mx+b$ except that $m$ is a matrix and $b$ is a vector.

Create a two-step Keras Sequential model again with the first layer being `normalizer` (`tf.keras.layers.Normalization(axis=-1)`) you defined earlier and adapted to the whole dataset:
"""

linear_model_MATH = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1)
])

linear_model_WRITING = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1)
])

linear_model_READING = tf.keras.Sequential([
    normalizer,
    layers.Dense(units=1)
])

linear_model_MATH.predict(train_features[:10])
linear_model_WRITING.predict(train_features[:10])
linear_model_READING.predict(train_features[:10])

"""When you call the model, its weight matrices will be built???check that the `kernel` weights (the $m$ in $y=mx+b$) have a shape of `(9, 1)`:"""

linear_model_MATH.layers[1].kernel
linear_model_WRITING.layers[1].kernel
linear_model_READING.layers[1].kernel

"""Configure the model with Keras `Model.compile` and train with `Model.fit` for 100 epochs:"""

linear_model_MATH.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

linear_model_WRITING.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

linear_model_READING.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1),
    loss='mean_absolute_error')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_MATH = linear_model_MATH.fit(
#     train_features,
#     train_labels_MATH,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.25)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_WRITING = linear_model_WRITING.fit(
#     train_features,
#     train_labels_WRITING,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.25)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_READING = linear_model_READING.fit(
#     train_features,
#     train_labels_READING,
#     epochs=100,
#     # Suppress logging.
#     verbose=0,
#     # Calculate validation results on 20% of the training data.
#     validation_split = 0.25)

"""Collect the results on the test set for later:"""

test_results['linear_model_MATH'] = linear_model_MATH.evaluate(
    test_features, test_labels_MATH, verbose=0)

test_results['linear_model_WRITING'] = linear_model_WRITING.evaluate(
    test_features, test_labels_WRITING, verbose=0)

test_results['linear_model_MATH'] = linear_model_READING.evaluate(
    test_features, test_labels_READING, verbose=0)

"""## Regression with a deep neural network (DNN)

In the previous section, you implemented two linear models for single and multiple inputs.

Here, you will implement single-input and multiple-input DNN models.

The code is basically the same except the model is expanded to include some "hidden" non-linear layers. The name "hidden" here just means not directly connected to the inputs or outputs.

These models will contain a few more layers than the linear model:

* The normalization layer, as before (with `studypower_normalizer` for a single-input model and `normalizer` for a multiple-input model).
* Two hidden, non-linear, `Dense` layers with the ReLU (`relu`) activation function nonlinearity.
* A linear `Dense` single-output layer.

Both models will use the same training procedure so the `compile` method is included in the `build_and_compile_model` function below.
"""

def build_and_compile_model(norm):
  model = keras.Sequential([
      norm,
      layers.Dense(64, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(1)
  ])

  model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(0.001))
  return model

"""### Regression using a DNN and a single input

Create a DNN model with only `'Studied'` as input and `studypower_normalizer` (defined earlier) as the normalization layer:
"""

dnn_studypower_model_MATH = build_and_compile_model(studyPower_normalizer)
dnn_studypower_model_WRITING = build_and_compile_model(studyPower_normalizer)
dnn_studypower_model_READING = build_and_compile_model(studyPower_normalizer)

"""This model has quite a few more trainable parameters than the linear models:"""

dnn_studypower_model_MATH.summary()
dnn_studypower_model_WRITING.summary()
dnn_studypower_model_READING.summary()

"""Train the model with Keras `Model.fit`:"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_MATH = dnn_studypower_model_MATH.fit(
#     train_features['Studied'],
#     train_labels_MATH,
#     validation_split=0.25,
#     verbose=0, epochs=100)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_WRITING = dnn_studypower_model_WRITING.fit(
#     train_features['Studied'],
#     train_labels_WRITING,
#     validation_split=0.25,
#     verbose=0, epochs=100)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_READING = dnn_studypower_model_READING.fit(
#     train_features['Studied'],
#     train_labels_READING,
#     validation_split=0.25,
#     verbose=0, epochs=100)

"""Collect the results on the test set for later:"""

test_results['dnn_studypower_model_MATH'] = dnn_studypower_model_MATH.evaluate(
    test_features['Studied'], test_labels_MATH,
    verbose=0)

test_results['dnn_studypower_model_WRITING'] = dnn_studypower_model_WRITING.evaluate(
    test_features['Studied'], test_labels_WRITING,
    verbose=0)

test_results['dnn_studypower_model_READING'] = dnn_studypower_model_READING.evaluate(
    test_features['Studied'], test_labels_READING,
    verbose=0)

"""### Regression using a DNN and multiple inputs

Repeat the previous process using all the inputs. The model's performance slightly improves on the validation dataset.
"""

dnn_model_MATH = build_and_compile_model(normalizer)
dnn_model_MATH.summary()

dnn_model_WRITING = build_and_compile_model(normalizer)
dnn_model_WRITING.summary()

dnn_model_READING = build_and_compile_model(normalizer)
dnn_model_READING.summary()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_MATH = dnn_model_MATH.fit(
#     x = train_features, y = train_labels_MATH,
#      epochs = 100, verbose = '0', validation_split = 0.2
#     )

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_WRITING = dnn_model_WRITING.fit(
#     x = train_features, y = train_labels_WRITING,
#      epochs = 100, verbose = '0', validation_split = 0.2
#     )

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history_READING = dnn_model_READING.fit(
#     x = train_features, y = train_labels_READING,
#      epochs = 100, verbose = '0', validation_split = 0.2
#     )

"""Collect the results on the test set:"""

test_results['dnn_model_MATH'] = dnn_model_MATH.evaluate(test_features, test_labels_MATH, verbose=0)
test_results['dnn_model_WRITING'] = dnn_model_WRITING.evaluate(test_features, test_labels_WRITING, verbose=0)
test_results['dnn_model_READING'] = dnn_model_READING.evaluate(test_features, test_labels_READING, verbose=0)

"""## Performance

Since all models have been trained, you can review their test set performance:
"""

pd.DataFrame(test_results, index=['Mean absolute error']).T

"""### Make predictions

You can now make predictions with the `dnn_model_XXXXX` on the test set using Keras `Model.predict` and review the loss:
"""

test_predictions_MATH = dnn_model_MATH.predict(test_features).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels_MATH, test_predictions_MATH)
plt.xlabel('True Values [Math Score]')
plt.ylabel('Predictions [Math Score]')
lims = [0, 100]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)

test_predictions_WRITING = dnn_model_WRITING.predict(test_features).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels_WRITING, test_predictions_WRITING)
plt.xlabel('True Values [WRITING Score]')
plt.ylabel('Predictions [WRITING Score]')
lims = [0, 100]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)

test_predictions_READING = dnn_model_READING.predict(test_features).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels_READING, test_predictions_READING)
plt.xlabel('True Values [READING Score]')
plt.ylabel('Predictions [READING Score]')
lims = [0, 100]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)

"""It appears that the model predicts reasonably well.

Now, check the error distribution:
"""

error = test_predictions_MATH - test_labels_MATH
print(test_predictions_MATH)
plt.hist(error, bins=25)
plt.xlabel('Prediction Error [MATH SCORE]')
_ = plt.ylabel('Count')

error = test_predictions_WRITING - test_labels_WRITING
print(test_predictions_WRITING)
plt.hist(error, bins=25)
plt.xlabel('Prediction Error [MATH SCORE]')
_ = plt.ylabel('Count')

error = test_predictions_READING - test_labels_READING
print(test_predictions_READING)
plt.hist(error, bins=25)
plt.xlabel('Prediction Error [MATH SCORE]')
_ = plt.ylabel('Count')
