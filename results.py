#importing python file dependencies
from tensorflowinit import model_chosen, test_accuracy
from update_gs import diagnosis_input

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
spreadsheet_id = '13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8'
service = build('sheets', 'v4', credentials=creds)

#get values from spreadsheet
gc = gspread.authorize(creds)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8/edit#gid=1737311642')
wks = sh.worksheet('Diagnosis_Input')
data = wks.get_all_values()
headers = data.pop(0)

#creating dataframe
df = pd.DataFrame(data, columns=headers)
ds = df.values

#defining values
properties = list(df.columns.values)
X = ds[properties]

#one hot encoding
Encoder = OneHotEncoder()
ct = ColumnTransformer([('encoder', OneHotEncoder(), [20])], remainder='passthrough')
diagnosis_input = np.array(ct.fit_transform(diagnosis_input), dtype=np.integer)

#get last row added
rows = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range).execute().get('values', [])
last_row = rows[-1] if rows else None
last_row_id = len(rows)
print(last_row_id, last_row)

#one hot encoding
Encoder = OneHotEncoder()
ct = ColumnTransformer([('encoder', OneHotEncoder(), [21])], remainder='passthrough')
diagnosis_input = np.array(ct.fit_transform(diagnosis_input), dtype=np.integer)

a= np.array([[diagnosis_input]])
print(model.predict(a))
