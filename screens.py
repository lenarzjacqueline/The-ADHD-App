from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.label import MDLabel
from kivymd.app import App
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from entry import Entry
from selection import Selection
from registerdata import Registerdata
from registerdiagnosis import Registerdiagnosis
from tried_n_failed.data import Data
from diagnosis import Diagnosis
from moreinfo import Moreinfo
from results import Results



class Screens(ScreenManager):
    layout = MDBoxLayout(orientation='vertical')

    def __init__(self, **kwargs):
        super(Screens, self).__init__(**kwargs)
        self.add_widget(Entry(name='entry'))
        self.add_widget(Selection(name='selection'))
        self.add_widget(Registerdata(name='registerdata'))
        self.add_widget(Registerdiagnosis(name='registerdiagnosis'))
        self.add_widget(Data(name='data'))
        self.add_widget(Diagnosis(name='diagnosis'))
        self.add_widget(Moreinfo(name='moreinfo'))
        self.add_widget(Results(name='results'))



