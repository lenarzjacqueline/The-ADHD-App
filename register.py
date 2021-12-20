#importing python file dependencies
from tensorflowinit import model_chosen, test_loss, test_acc, chosen_mse, chosen_std
from update_gs import diagnosis_input
from main import MainApp

#importing dependencies for our kv screen information
from google.oauth2 import service_account
from kivy.lang import builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy import widget
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivy.uix.widget import Widget

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

#get spreadsheet and pertinent values - DIAGNOSIS DF
gc = gspread.authorize(creds)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8/edit#gid=1737311642')
wk_2 = sh.get_worksheet('Diagnosis_Input')
data = wk_2.get_all_values()
headers = data.pop(0)
ethnicity = wk_2.cell(21, 1).value

#one hot encoding - manually (delete value - keep the property titles)
#then add new encoded values to match train and test data
wk_2.delete_value(21, 1, number=1, values=None, inherit=False)
wk_2.insert_cols(21, number=3, values=None, inherit=False)
if ethnicity == 1:
    wk_2.insert_rows(row = 1, number = 3, values =['1', '0', '0'])
elif ethnicity == 2:
    wk_2.insert_rows(row = 1, number = 3, values =['0', '1', '0'])
elif ethnicity == 3:
    wk_2.insert_rows(row = 1, number = 3, values =['0', '0', '1'])
else: 
    wk_2.insert_rows(row = 1, number = 3, values =['0', '0', '1'])

#create pandas df from data
data = wk_2.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
ds = df.values
properties = list(df.columns.values)
X = ds[properties]

#generate prediction using numpy array and chosen model
a= np.array([[X]])
classification = model_chosen.predict(a)


#delete sheet for next user, add info to combined sheet and delete blank property tabs added into Diagnosis_Input and delete sheet for next user
if classification != 0:
    wk_3 = sh.get_worksheet('Diag_Raw_Combined')
    wk_4 = sh.get_worksheet('Diag_Raw')
    wk_5 = sh.get_worksheet('ML_Model_Used')
    wk_3.insert_row(values = [X, classification])
    wk_4.insert_rows(values = [X, classification, '1', model_chosen, chosen_mse, chosen_std, test_loss, test_acc])
    wk_5.insert_rows(values = [model_chosen, chosen_mse, chosen_std, test_loss, test_acc, classification])
    wk_2.delete_columns(22,23)
    wk_2.delete_row(1)

class ResultsSplashscreen(Screen):
    def on_start(self):
        Clock.schedule_once(self.change_screen,4)
    def change_screen(self, dt):
        MainApp.root.current = 'results'

class RestultsButton(MDRaisedButton):
    def build(self):
        self.resultsbtn = 'resultsbtn' 

def print_it(instance, value):
    print('*remember this is not offical*/n', classification)
widget = RestultsButton(text='Show Results', markup=True)
widget.bind(on_ref_press=print_it)
