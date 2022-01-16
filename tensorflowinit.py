#importing python dependencies
from keras.engine.input_layer import InputLayer
from main import Mainapp, ScreenManager, Screen

#importing dependencies for our kv screen information
import kivy
import kivymd
from google.oauth2 import service_account
from kivy.uix.screenmanager import ScreenManager, Screen

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
from keras.models import Sequential, Model
from keras import backend as K
from keras.layers import LSTM, Dense, Bidirectional, Input, Dropout, BatchNormalization, CuDNNLSTM, GRU, CuDNNGRU, Embedding, GlobalMaxPooling1D, GlobalAveragePooling1D, Flatten
from keras.wrappers.scikit_learn import KerasRegressor, KerasClassifier
from sklearn.model_selection import cross_val_score, train_test_split, KFold, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score
from sklearn import svm
import numpy as np
from numpy import std, mean


####code####


#authorizaiton to read
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#open gsheets
sh = client.open('ADHD App API')
wk_1 = client.open("ADHD App API").get_worksheet(0)
data = wk_1.get_all_values()
headers = data.pop(0)

#row count of data sheet
rowcountdata = wk_1.row_count 

# define base model - BCE 
def model_baseline():
  inputs = Input(shape=(30,))
  dense = Dense(4, activation=tf.nn.relu)(inputs)
  dense1 = Dense(16, activation=tf.nn.relu)(dense)
  dense2 = Dense(16, activation=tf.nn.relu)(dense1)
  outputs = Dense(1, activation=tf.nn.sigmoid)(dense2)
  model_baseline = Model(inputs=inputs, outputs=outputs)
  model_baseline.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model_baseline

#evaluate a smaller network
def model_smaller():
  inputs = Input(shape=(30,))
  x = Dense(4, activation=tf.nn.relu)(inputs)
  outputs = Dense(1, activation=tf.nn.sigmoid)(x)
  model_smaller = Model(inputs=inputs, outputs=outputs)
  model_smaller.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model_smaller
      
#SVM model
def SVM_Model(X_train, Y_train, X_test):
  clf = svm.SVC(gamma=0.001, C=100.)
  clf.fit(X_train, Y_train)
  predictions = clf.predict(X_test)
  return predictions
        
#defining our values to be passed to next screen and initiating our training / testing to produce said values
class MLAlgo():
  def __init__(self):
    self.model_chosen = None
    self.mse_chosen = None
    self.std_chosen = None
    self.test_loss = None
    self.test_acc = None
      
  def build(self):
    if wk_1.row_count < 100:
      self.parent.current = "notenoughinfo"
    else: #input into tensorflow for classification
      
      # shuffle the dataset
      df = pd.DataFrame(data, columns=headers)
      df = df.astype(int)
      df = df.sample(frac=1).reset_index(drop=True)

      # split into input (X) and output (Y) variables
      X = df.copy()
      Y = X.pop('adhd')

      #split to train and test data
      X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=1)

      kfold = StratifiedKFold(n_splits=3, shuffle=True)

      # evaluate baseline model with standardized dataset
      estimators_standard = [
        ('standardize', StandardScaler()),
        ('mlp', KerasClassifier(
          build_fn=model_baseline, 
          epochs=250, 
          batch_size=33,
          validation_split=0.33,
          validation_freq=10,
          verbose=1,
          callbacks=[
            keras.callbacks.TensorBoard(log_dir='/Users/jacquelenarz/Desktop/school/logs/model_baseline'),
            tf.keras.callbacks.EarlyStopping(
              monitor="val_acc",
              min_delta=0.02,
              patience=40,
              mode="max",
              restore_best_weights=True,
            ) 
          ],
          use_multiprocessing=True,
          workers=4
          ))
      ]
      
      pipeline_standard = Pipeline(estimators_standard)
      pipeline_standard.fit(X_train, Y_train)
      results = cross_val_score(pipeline_standard, X, Y, cv=kfold)
      results_standardized_mean = np.mean(results)
      results_standardized_std = np.std(results)
        
      # evaluate smaller model
      estimators_smaller = [
        ('standardize', StandardScaler()),
        ('mlp', KerasClassifier(
          build_fn=model_smaller,
          epochs=250,
          batch_size=33,
          validation_split=0.33,
          validation_freq=10,
          verbose=1, 
          callbacks=[
            keras.callbacks.TensorBoard(log_dir='/Users/jacquelenarz/Desktop/school/logs/model_smaller'),
            tf.keras.callbacks.EarlyStopping(
              monitor="val_acc",
              min_delta=0.02,
              patience=40,
              mode="max",
              restore_best_weights=True,
            ) 
          ],
          use_multiprocessing=True,
          workers=4
          ))
      ]
      pipeline_smaller = Pipeline(estimators_smaller)
      pipeline_smaller.fit(X_train, Y_train)
      results = cross_val_score(pipeline_smaller, X, Y, cv=kfold)
      results_smaller_mean = np.mean(results)
      results_smaller_std = np.std(results)
      
      # evaluate svm model
      estimators_svm = [
        ('standardize', StandardScaler()),
        ('svm', svm.SVC(gamma=0.001, C=100., probability=True))
      ]
      pipeline_svm = Pipeline(estimators_svm)
      pipeline_svm.fit(X_train, Y_train)
      results = cross_val_score(pipeline_svm, X, Y, cv=kfold)
      results_svm_mean = np.mean(results)
      results_svm_std = np.std(results)
      
      models = [pipeline_standard, pipeline_smaller, pipeline_svm]
      results_mean = [results_standardized_mean, results_smaller_mean, results_svm_mean]
      results_std = [results_standardized_std, results_smaller_std, results_svm_std]

      self.model_chosen = models[np.argmax(results_mean)]
      self.mse_chosen = np.max(results_mean)
      self.std_chosen = results_std[np.argmax(results_mean)]

