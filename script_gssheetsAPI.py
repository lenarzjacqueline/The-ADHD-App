#importing google dependencies
import gspread
from gspread.models import Worksheet
import googleapiclient
import pygsheets
from google.auth.transport.requests import Request
from oauth2client.service_account import ServiceAccountCredentials


#importing kv dependencies
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, ButtonBehavior

#importing classes to work with
from main import MainApp


#authorizing/loading API
gc = pygsheets.authorize(service_file='/Users/jacquelenarz/Downloads/client_secret.json')



#creating the link to the spreadsheet and creating sheets within
sh = gc.open('ADHD App API')
wk_1 = sh.get_worksheet('Data_Input')
wk_2 = sh.get_worksheet('Diagnosis_Input')
wk_3 = sh.get_worksheet('Diag_Raw')
wk_4 = sh.get_worksheet('Diag_Raw_Comnbined')
wk_5 = sh.get_worksheet('ML_Models')
wk_6 = sh.get_worksheet('Email')


#opening data input wks to see if we have enough data to run our algo to diagnose respondant
wk_1.row_count = []

#defining the options for amount of data we have
def change_screen_no(MainApp, dt):
    MainApp.root.current = 'notenoughinfo'
def change_screen_yes(MainApp, dt):
    MainApp.root.current = 'diagnosis'

#preparing direction of data / diagnosis building
class Selection(Screen):
    #creating button to see if enough data has been input to even run the algorithm
    def change_screen_no(MainApp, dt):
        MainApp.root.current = 'notenoughinfo'
    def change_screen_yes(MainApp, dt):
        MainApp.root.current = 'diagnosis'
    def diagbtn(MDFlatButton):
        MDFlatButton.diagbtn = 'diagbutn'
    def on_press(diagbtn):
            if wk_1.row_count > 100:
                change_screen_yes
            if wk_1.row_count < 100:
                change_screen_no
