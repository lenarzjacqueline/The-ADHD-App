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

#get spreadsheet and pertinent values
gc = gspread.authorize(creds)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8/edit#gid=1737311642')
wks = sh.get_worksheet('Diagnosis_Input')
data = wks.get_all_values()
headers = data.pop(0)
ethnicity = wks.cell(21, 1).value

#one hot encoding - manually (delete value - keep the property titles)
#then add new encoded values to match train and test data
wks.delete_values(21, 1, number=1, values=None, inherit=False)
wks.insert_cols(21, number=3, values=None, inherit=False)
if ethnicity == 1:
    wks.insert_rows(row = 1, number = 3, values =['1', '0', '0'])
elif ethnicity == 2:
    wks.insert_rows(row = 1, number = 3, values =['0', '1', '0'])
elif ethnicity == 3:
    wks.insert_rows(row = 1, number = 3, values =['0', '0', '1'])
else: 
    wks.insert_rows(row = 1, number = 3, values =['0', '0', '1'])

#create pandas pf
data = wks.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
ds = df.values
properties = list(df.columns.values)
X = ds[properties]

#generate prediction using numpy array and chosen model
a= np.array([[X]])
print(model_chosen.predict(a))


#delete sheet for next user, delete blank property tabs added
if model_chosen.predict(a) != 0:
    wks.delete_columns(22,23)
    wks.delete_row(1)
