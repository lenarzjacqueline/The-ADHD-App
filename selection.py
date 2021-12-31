#importing google dependencies
import gspread
from gspread.models import Worksheet
import googleapiclient
from kivy.app import App
import pygsheets
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials


#importing kv dependencies
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, ButtonBehavior

#importing classes to work with
from main import Mainapp


#authorizing/loading API
#gc = pygsheets.authorize(service_file='/Users/jacquelenarz/Downloads/client_secret.json')

#authorizaiton to read
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#open gsheets
sh = client.open('ADHD App API')
wk_1 = client.open("ADHD App API").get_worksheet(0)


#preparing direction of data / diagnosis building
class Selection(Screen):
    #creating button to see if enough data has been input to even run the algorithm
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def diagnosis_btn (self):
        if wk_1.row_count > 100:
            Mainapp.parent.current = 'diagnosis'
        if wk_1.row_count < 100:
            Mainapp.parent.current = 'notenoughinfo'

