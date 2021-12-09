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
import tensorflow
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

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
X = ds[:,0:29]
Y = ds[:,30]

# define base model
def baseline_model():
      
	# create model
	model = Sequential()
	model.add(Dense(13, input_dim=13, kernel_initializer='normal', activation='relu'))
	model.add(Dense(1, kernel_initializer='normal'))
 
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model

# evaluate model
estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)
kfold = KFold(n_splits=10)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))
