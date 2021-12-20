#importing dependencies for our kv screen information
from google.oauth2 import service_account
from kivy.lang import builder

#importing gsheets dependencies
import os
import sys
import gspread
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.textinput import TextInput
from pyobjus import autoclass
import pygsheets
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#importing ML dependencies
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras import layers, models, Sequential, optimizers, initializers, regularizers, constraints
from keras.models import Sequential
from keras import backend as K
from keras.layers import LSTM, Dense, Bidirectional, Input, Dropout, BatchNormalization, CuDNNLSTM, GRU, CuDNNGRU, Embedding, GlobalMaxPooling1D, GlobalAveragePooling1D, Flatten
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from sklearn.model_selection import cross_val_score, train_test_split, KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.datasets.samples_generator import make_blobs
from sklearn.metrics import accuracy_score
from sklearn import svm
import numpy as np
from numpy import std, mean

#authorizaiton to read
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#open gsheets
sh = client.open('ADHD App API')
wk_1 = client.open("ADHD App API").get_worksheet(1)
data = wk_1.get_all_values()
headers = data.pop(0)

#DATA DF
df = pd.DataFrame(data, columns=headers)
ds = df.values

# split into input (X) and output (Y) variables
properties = list(df.columns.values)
properties.remove('adhd_data')

X = ds[properties]
Y = ds['adhd_data']


# shuffle the dataset
ds = ds.sample(frac=1).reset_index(drop=True)

# convert to numpy arrays
X = np.array(X)

#add df to gsheets combined once in np array, pasting in adhd classification, noting it is "data" data in wks_4
wk_3 = sh.worksheet('Data_Raw_Combined')
wk_3.insert_row(values = [X, 'adhd_data', '0'])

#one hot encoding
Encoder = OneHotEncoder()
ct = ColumnTransformer([('encoder', OneHotEncoder(), [22])], remainder='passthrough')
X = np.array(ct.fit_transform(X), dtype=np.integer)

#split to train and test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=1)


# define base model - BCE 
def model_baseline():
  modelstandard = Sequential([
    keras.layers.Flatten(input_shape=(4,)),
    keras.layers.Dense(16, activation=tf.nn.relu),
	  keras.layers.Dense(16, activation=tf.nn.relu),
    keras.layers.Dense(1, activation=tf.nn.sigmoid),
])
  modelstandard.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
  return modelstandard

# evaluate baseline model with standardized dataset
estimators_standard = []
estimators_standard.append(('standardize', StandardScaler()))
estimators_standard.append(('mlp', KerasClassifier(build_fn=model_baseline, epochs=100, batch_size=5, verbose=0)))
pipeline_standard = Pipeline(estimators_standard)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(pipeline_standard, X, Y, cv=kfold)
results_standardized_mean = results.mean()*100
results_standardized_std = results.std()*100


#evaluate a smaller network
def model_smaller():
  modelsmaller = Sequential()
  modelsmaller.add(Dense(30, input_dim=60, activation=tf.nn.relu))
  modelsmaller.add(Dense(1, activation=tf.nn.sigmoid))
  modelsmaller.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return modelsmaller
  
# evaluate smaller model - BCE
estimators_smaller = []
estimators_smaller.append(('standardize', StandardScaler()))
estimators_smaller.append(('mlp', KerasClassifier(build_fn=model_smaller, epochs=100, batch_size=5, verbose=0)))
pipeline_smaller = Pipeline(estimators_smaller)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(pipeline_smaller, X, Y, cv=kfold)
results_smaller_mean = results.mean()*100
results_smaller_std = results.std()*100


#SVM model
def SVM_Model():
  clf = svm.SVC(gamma=0.001, C=100.)
  clf.fit(X_train, Y_train)
  #configuration options
  blobs_random_seed = 42
  centers = [(0,0), (5,5)]
  cluster_std = 1
  frac_test_split = 0.33
  num_features_for_samples = 2
  num_samples_total = 1000
  inputs, targets = make_blobs(n_samples = num_samples_total, centers = centers, n_features = num_features_for_samples, cluster_std = cluster_std)
  predictions = clf.predict(X_test)


#choose our model
if results_standardized_mean > results_smaller_mean:
  model_chosen = model_smaller
  chosen_mse = results_smaller_mean
  chosen_std = results_smaller_std
else:
  model_chosen = model_baseline
  chosen_mse = results_standardized_mean
  chosen_std = results_standardized_std



#creating epochs with our chosen model
model_chosen.fit(X_train, Y_train, epochs=50, batch_size=1)


#loss functiton - bce
test_loss, test_acc = model_chosen.evaluate(X_test, Y_test)  
