#importing python file dependencies
from tensorflowinit import MLAlgo
from main import Mainapp

#importing dependencies for our kv screen information
from kivy.lang import builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout  
from kivy.uix.textinput import TextInput
 

#importing gsheets dependencies
import os
import sys
import gspread
import oauth2client
from google.oauth2 import service_account
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
import pickle
import os.path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

#importing ML dependencies
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
from numpy import std, mean


####code####


#authorizaiton to read
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#open gsheets
sh = client.open('ADHD App API')
wk_2 = client.open("ADHD App API").get_worksheet(1)
data = wk_2.get_all_values()
headers = data.pop(0)

#create pandas df from data
data = wk_2.get_all_values()
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers, dtype=float)

# split into input (X) variable
X = df.copy()

#define our function from tensorflow file
diagnosis = MLAlgo()
diagnosis.build()

#calculate actual probability of ADHD
proba = diagnosis.model_chosen.predict_proba(X)[0]
proba = proba[1]*100
classification = f'You have {proba:.2f}% chance of having ADHD'

