#import relavent py files
from main import Mainapp, App

#import relavent dependencies
from kivy.lang import Builder
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivymd.uix.screen import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config 
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
import kivy.utils
from kivy.utils import platform
from kivy.properties import NumericProperty

import kivymd
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager

from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationErrorCache, MDBottomNavigationItem, MDTab, MDBottomNavigationHeader
from kivymd.uix.boxlayout import MDBoxLayout   
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton, ButtonBehavior
from kivymd.uix.dialog import MDDialog 
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem,ThreeLineListItem
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField


#import gsheets
import os
import sys
import gspread
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2 import service_account
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

from real_workspace.result import X


####code####


#authorizaiton to edit & opening pertinent pages
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#defining last row for our gsheets
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

#check if email already registered, if yes pop up and go back to home
class RegisterDiagnosis(Screen):
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
