from Google import Create_Service
import pandas as pd
import numpy as np
from google_auth_oauthlib.flow import InstalledAppFlow 

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
gsheetId = '13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8'

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

