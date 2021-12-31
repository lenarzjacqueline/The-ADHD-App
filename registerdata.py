#import relavent py files
from main import Mainapp, ScreenManager, App

#import relavent dependencies
from kivy.lang import builder
from kivymd.uix.screen import MDScreen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.button import Button, ButtonBehavior
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, ButtonBehavior
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivymd.uix.screen import Screen
from kivy.uix.widget import Widget


#import gsheets
import gspread
from gspread import cell_list , worksheet
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np


####code####

#authorizaiton to edit
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#defining last row for our gsheets
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


#creating the link to the spreadsheet to refer to and update
sa = gspread.service_account(filename='service_account.json')
sh = sa.open('ADHD App API')
wk_5 = sh.worksheet("Emails")


#check if email already registered, if yes pop up and go back to home
class RegisterData(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #check if age between 18-35, if no pop up and go back to home            
    def email_on_press(self):
        email = self.email.text
        x = [email]
        wk_5 = client.open("ADHD App API").worksheet("Emails")
        next_row = next_available_row(wk_5)
        cell_list = wk_5.findall(x)
        if cell_list == ['None']:
            wk_5.update(f'A{next_row}', [x]) 
            wk_5.sort_range(range, basecolumnindex=0, sortorder='ASCENDING')
        else: 
            Mainapp.root.current = "popup"
    #check if age between 18-35, if no pop up and go back to home            
    def age_on_press(self):
        age = self.age.text
        y = [age]
        y = NumericProperty(y)
        if y < 18: 
            Mainapp.root.current = "popup"
