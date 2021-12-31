#importing python functions
import pickle
from plyer.facades import notification
import uvicorn
from fontTools.ttLib import TTFont
from functools import partial
import webbrowser

#importing Kivy and KivyMD (alphabetical)
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

#importing API functions for googlesheets
import os
import sys
import gspread
from google.oauth2 import service_account

#importing tensorflow ML functions
import tensorflow
from tensorflow import keras
import pandas as pd
import numpy as np

kivy.require('1.9.1')



####code####



#building call to popup function for validation of user info / research data user profile
class Popup(Screen):
    pass
   
    
#class to define numeric input, as an inheritence of textinput
class NumericInput(TextInput):
    min_value = NumericProperty()
    max_value = NumericProperty()
    def __init__(self, *args, **kwargs):
        TextInput.__init__(self, *args, **kwargs)
        self.input_filter = 'float'
        self.multiline = False

    def insert_text(self, string, from_undo=False):
        new_text = self.text + string
        if new_text != "":
            if self.min_value <= float(new_text) <= self.max_value:
                TextInput.insert_text(self, string, from_undo=from_undo)


#class to create hyperlink to website
class Hyperlink(Label):
    def __init__(self, **kwargs):
      self.target = kwargs.pop('target')
      kwargs['markup'] = True
      kwargs['color'] = (0,0,1,1)
      kwargs['text'] = "[u][ref=https://theadhdapp.com/]{}[/ref][/u]".format(kwargs['text'])
      kwargs['on_ref_press'] = self.link
      super().__init__(**kwargs)
    def link(self, *args):
      webbrowser.open(self.target)


#buidling classes for our screens that have no seperate py page, inheriting from Screen class to be controlled by ScreenManager
class Entry(Screen):
    pass

class Selection(Screen):
    pass

class Moreinfo(Screen):
    pass

class ThankYou(Screen):
    pass

class NotEnoughInfo(Screen):
    pass

class PrivacyPolicy(Screen):
    pass

class Prediction(Screen):
    pass

class ResultsSplashScreen(Screen):
    pass

#screen manager
class WindowManager(ScreenManager):
    pass


#building GUI
class Mainapp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("entry.kv"))
        sm.add_widget(Builder.load_file("selection.kv"))
        sm.add_widget(Builder.load_file("privacypolicy.kv"))
        sm.add_widget(Builder.load_file("notenoughinfo.kv"))
        sm.add_widget(Builder.load_file("registerdata.kv"))
        sm.add_widget(Builder.load_file("registerdiagnosis.kv"))
        sm.add_widget(Builder.load_file("popup.kv"))
        sm.add_widget(Builder.load_file("thankyou.kv"))
        sm.add_widget(Builder.load_file("data.kv"))
        sm.add_widget(Builder.load_file("data_two.kv"))
        sm.add_widget(Builder.load_file("data_three.kv"))
        sm.add_widget(Builder.load_file("data_four.kv"))
        sm.add_widget(Builder.load_file("data_five.kv"))
        sm.add_widget(Builder.load_file("data_submit.kv"))
        sm.add_widget(Builder.load_file("diagnosis.kv"))
        sm.add_widget(Builder.load_file("diagnosis_two.kv"))
        sm.add_widget(Builder.load_file("diagnosis_three.kv"))
        sm.add_widget(Builder.load_file("diagnosis_four.kv"))
        sm.add_widget(Builder.load_file("diagnosis_five.kv"))
        sm.add_widget(Builder.load_file("diagnosis_submit.kv"))
        sm.add_widget(Builder.load_file("moreinfo.kv"))
        sm.add_widget(Builder.load_file("resultssplashscreen.kv"))
        sm.add_widget(Builder.load_file("prediction.kv"))
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.accent_palette = 'Pink'
        self.theme_cls.theme_style = 'Dark'
        self.title = "The ADHD App"
        return sm
    def on_start(self):
        Clock.schedule_once(self.change_screen,8)
    def change_screen(self, dt):
        self.root.current = 'selection'


if __name__ == "__main__" :
    Mainapp().run()
