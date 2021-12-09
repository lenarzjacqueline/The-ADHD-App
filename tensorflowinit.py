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
from sklearn.metrics import accuracy_score
import numpy as np
from numpy import std, mean

#authorizaiton to read
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfilename('service_account.json', scope)
gc = pygsheets.authorize(creds)


gc = gspread.authorize(creds)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8/edit#gid=1737311642')
wks = sh.worksheet('Data_Input')
data = wks.get_all_values()
headers = data.pop(0)

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

#split to train and test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=1)

#one hot encoding
Encoder = OneHotEncoder()
ct = ColumnTransformer([('encoder', OneHotEncoder(), [21])], remainder='passthrough')
X = np.array(ct.fit_transform(X), dtype=np.integer)

# define base model
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
    	# create model
  modelsmaller = Sequential()
  modelsmaller.add(Dense(30, input_dim=60, activation='relu'))
  modelsmaller.add(Dense(1, activation='sigmoid'))
  modelsmaller.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return modelsmaller
  
# evaluate smaller model
estimators_smaller = []
estimators_smaller.append(('standardize', StandardScaler()))
estimators_smaller.append(('mlp', KerasClassifier(build_fn=model_smaller, epochs=100, batch_size=5, verbose=0)))
pipeline_smaller = Pipeline(estimators_smaller)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(pipeline_smaller, X, Y, cv=kfold)
results_smaller_mean = results.mean()*100
results_smaller_std = results.std()*100


if results_standardized_mean > results_smaller_mean:
  model_chosen = model_baseline
  

model_chosen.fit(X_train, Y_train, epochs=50, batch_size=1)


test_loss, test_acc = model_chosen.evaluate(X_test, Y_test)  
test_accuracy = ('Test accuracy:', test_acc)
