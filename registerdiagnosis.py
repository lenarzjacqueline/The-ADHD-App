#import relavent py files
from main import popupWindow, MainApp, ScreenManager, Diagnosis, RegisterDiagnosis

#import relavent dependencies
import kivy
import kivymd
from kivy import builder
from kivymd import Screen
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.button import Button, ButtonBehavior
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, ButtonBehavior


#import gsheets
import gspread
from gspread import cell_list , worksheet
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pygsheets




#setting up our API credentials to read and write
SCOPES = ['https://googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(
    'service_account.json', scopes=SCOPES)
client = gspread.authorize(creds)
API_SERVICE_NAME = 'sheets'
SPREADSHEET_ID = '13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8'

service = build('sheets', 'v4', credentials=creds)


#creating the link to the spreadsheet to refer to and update
sa = gspread.service_account(filename='service_account.json')
sh = sa.open('ADHD App API')
wk_5 = sh.worksheet("Emails")


#check if email already registered, if yes pop up and go back to home
class Registerdiagnosis(Screen):
    container = ObjectProperty(None)
    data_list = ListProperty([])
    def build(self):
        builder.load_file('registerdiagnosis.kv')
    def save_data(self):
        for child in reversed(self.container.children):
            if isinstance(child, TextInput):
                self.data_list.append(child.text)
    #check if age between 18-35, if no pop up and go back to home            
    def agebtn(MDFlatButton):
        MDFlatButton.agebtn = 'agebtn'
    def on_press(agebtn):
        if 'age_check' < 18: 
            popupWindow.open()
        else: 
            MainApp.root.current = "diagnosis"
    #check if age between 18-35, if no pop up and go back to home            
    def emailbtn(MDFlatButton):
        MDFlatButton.emailbtn = 'emailbtn'
        email_match = print(cell_list(worksheet.findal("email_check")))
        if email_match == ['']:
            wk_5.insert_rows(row = wk_5.rows+1, number = 1, values =['email'])
            wk_5.sort_range(range, basecolumnindex=0, sortorder='ASCENDING')
            MainApp.root.current = "diagnosis"
        else: 
            popupWindow.open()
    #make sure respondant is female
    def malebtn(MDFlatButton):
        MDFlatButton.malebtn = 'genderbtn'
    def on_press(malebtn):
            popupWindow.open()
