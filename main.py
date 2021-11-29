#importing python functions
import pickle
import uvicorn
from fontTools.ttLib import TTFont

#importing Kivy
import kivy
import kivymd
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, ColorProperty, StringProperty
from kivy.clock import Clock, mainthread
from kivy.uix.textinput import TextInput
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
from kivymd.uix.list import OneLineListItem,ThreeLineListItem
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout   
from kivymd.uix.dialog import MDDialog 
from kivymd.uix.list import OneLineIconListItem
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivymd.uix.floatlayout import FloatLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationErrorCache, MDBottomNavigationItem, MDTab, MDBottomNavigationHeader
from kivymd.uix.label import MDLabel
from kivy.core.text import LabelBase
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

#importing API functions
import pandas as pd
import os
import gspread
from openpyxl import load_workbook


kivy.require('1.9.1')







#building call to popup function for validation
class PopupWindow(Widget):
    def btn(self):
        popFun()

class P(FloatLayout):
    pass

def popFun():
    show = P()
    window = Popup(title = "Oops", content = show,
                    size_hint = (None, None), size = (300,300))
    window.open()



#class to validate user info (data and diagnosis), accepting if no email similar and logging the data and clearing the login widget
class Registerdata(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    email = ObjectProperty(None)
    def registerbtn(self):
        user = pd.DataFrame([[self.first_name.text, self.last_name.text, self.email.text]],
                            columns = ['First Name', 'Last Name', 'Email'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
                user.to_csv('userinfo.csv', mode = 'a', header = False, index = False)
                self.first_name.text = ""
                self.last_name.text = ""
                self.email.text = ""
        else:
            popFun()
  
class Registerdiagnosis(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    email = ObjectProperty(None)
    def registerbtn(self):
  
        user = pd.DataFrame([[self.first_name.text, self.last_name.text, self.email.text]],
                            columns = ['First Name', 'Last Name', 'Email'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
                user.to_csv('userinfo.csv', mode = 'a', header = False, index = False)
                self.first_name.text = ""
                self.last_name.text = ""
                self.email.text = ""
        else:
            popFun()



#class to log the data from the data and diagnosis screens
class Data(Screen):
    pass

class Diagnosis(Screen):
    pass





#buidling classes for our screens
class Entry(Screen):
    pass

class Selection(Screen):
    pass

class Moreinfo(Screen):
    pass

class Results(Screen):
    pass

class Screen(ScreenManager):
    pass


#managing screens
sm = ScreenManager()
sm.add_widget(Entry(name='entry'))
sm.add_widget(Selection(name='selection'))
sm.add_widget(Registerdata(name='registerdata'))
sm.add_widget(Registerdiagnosis(name='registerdiagnosis'))
sm.add_widget(Data(name='data'))
sm.add_widget(Diagnosis(name='diagnosis'))
sm.add_widget(Moreinfo(name='moreinfo'))
sm.add_widget(Results(name='results'))


#reading the data stored as user info
users = pd.read_csv('userinfo.csv')


#building GUI
class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("entry.kv"))
        sm.add_widget(Builder.load_file("selection.kv"))
        sm.add_widget(Builder.load_file("registerdata.kv"))
        sm.add_widget(Builder.load_file("registerdiagnosis.kv"))
        sm.add_widget(Builder.load_file("data.kv"))
        sm.add_widget(Builder.load_file("diagnosis.kv"))
        sm.add_widget(Builder.load_file("moreinfo.kv"))
        sm.add_widget(Builder.load_file("results.kv"))
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