#importing python functions
import pickle
from plyer.facades import notification
import uvicorn
from fontTools.ttLib import TTFont
from functools import partial
from pprint import pprint
import webbrowser
from os.path import join,dirname

#importing Kivy and KivyMD (alphabetical)
import kivy
from kivy.animation import Animation
from kivy.app import App
from kivy.base import runTouchApp
from kivy.clock import Clock, mainthread
from kivy.config import Config 
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
import kivy_garden
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, ColorProperty, StringProperty, DictProperty
import kivy.utils
from kivy.utils import platform


import kivymd
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager

from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
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
from kivymd.uix.textfield import MDTextField


#importing API functions for googlesheets
import os
import sys
import gspread
from google.oauth2 import service_account
from openpyxl import load_workbook
import json
import requests

#importing tensorflow ML functions
import tensorflow
from tensorflow import keras
import pandas as pd
import numpy as np
import gradio as gr




kivy.require('1.9.1')

#scrolling screen class
class ScrollingScreen(Screen):
    container = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(ScrollingScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))
        self.add_text_inputs()

    def add_text_inputs(self):
        for x in range(35):
            self.container.add_widget(Label(text="Label {}".format(x), size_hint_y=None, height=40))


#building call to popup function for validation
class Popup(Widget):
    def btn(self):
        show_popup()

class P(FloatLayout):
    pass

def show_popup():
    show = P()
    popupWindow = Popup(title = "sorry!", content = show,
                    size_hint = (None, None), size = (300,300), autodismiss = False)
    popupWindow.open()
    
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



#classes to utilize the scrolling screen to log the data input
class Data(ScrollingScreen):
    pass

class Diagnosis(ScrollingScreen):
    pass
        


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



#buidling classes for our screens that have no py page
class Entry(Screen):
    pass

class Selection(Screen):
    pass

class Moreinfo(Screen):
    pass

class Results(Screen):
    pass

class ThankYou(Screen):
    pass

class NotEnoughInfo(Screen):
    pass

class PrivacyPolicy(Screen):
    pass


#screen manager
class Screen(ScreenManager):
    pass



#building GUI
class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("entry.kv"))
        sm.add_widget(Builder.load_file("selection.kv"))
        sm.add_widget(Builder.load_file("privacypolicy.kv"))
        sm.add_widget(Builder.load_file("notenoughinfo.kv"))
        sm.add_widget(Builder.load_file("registerdata.kv"))
        sm.add_widget(Builder.load_file("registerdiagnosis.kv"))
        sm.add_widget(Builder.load_file("data.kv"))
        sm.add_widget(Builder.load_file("diagnosis.kv"))
        sm.add_widget(Builder.load_file("moreinfo.kv"))
        sm.add_widget(Builder.load_file("resultssplashscreen.kv"))
        sm.add_widget(Builder.load_file("results.kv"))
        sm.add_widget(Builder.load_file("thankyou.kv"))
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.accent_palette = 'Pink'
        self.theme_cls.theme_style = 'Dark'
        self.title = "The ADHD App"
        return sm
    def on_start(self):
        Clock.schedule_once(self.change_screen,4)
    def change_screen(self, dt):
        self.root.current = 'selection'


if __name__ == "__main__" :
    MainApp().run()
    

