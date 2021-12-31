#importing dependencies for our kv screen information
from kivy.lang import Builder
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen, ScreenManager, FallOutTransition
from kivymd.uix.screen import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#importing other python files
import globalshared_diagnosis
import globalshared_data
from main import Mainapp, App

#importing gsheets dependencies
import os
import sys
import gspread
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2 import service_account
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

#update Data for testing and training - classes seperated by screens to be accessed by the kivy files associated
class Data(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def data_on_press(self):
        age = self.age.text
        adhd = self.adhd.text
        time = self.time.text 
        lead = self.lead.text
        decisions = self.decisions.text
        globalshared_data.x = [age, adhd, time, lead, decisions]
                    
class Data2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def data_two_on_press(self):
        depression = self.depression.text
        bipolar = self.bipolar.text
        anxiety = self.anxiety.text
        alcohol = self.alcohol.text
        crying = self.crying.text
        globalshared_data.y = [depression, bipolar, anxiety, alcohol, crying]
                      
class Data3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def data_three_on_press(self):
        headtraumas = self.headtraumas.text
        money = self.money.text
        impatient = self.impatient.text         
        parentsdiagnosed = self.parentsdiagnosed.text
        siblingsdiagnosed = self.siblingsdiagnosed.text
        globalshared_data.z = [headtraumas, money, impatient, parentsdiagnosed, siblingsdiagnosed]
    
class Data4(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def data_four_on_press(self):
        siblingsamount = self.siblingsamount.text
        siblingorder = self.siblingorder.text         
        autism = self.autism.text
        trauma = self.trauma.text
        wfh = self.wfh.text
        globalshared_data.a = [siblingsamount, siblingorder, autism, trauma, wfh]

class Data5(Screen):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def data_five_on_press(self):
        premature = self.premature.text       
        birthweight = self.birthweight.text
        ethnicity = self.ethnicity.text
        speedingticket = self.speedingticket.text
        publicoverwhelmed = self.publicoverwhelmed.text
        globalshared_data.b = [premature, birthweight, ethnicity, speedingticket, publicoverwhelmed]

class Data_Submit(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
    def data_submit_on_press(self):
        ed = self.ed.text
        imposter = self.imposter.text
        temper = self.temper.text
        appointments = self.appointments.text        
        concentratetalking = self.concentratetalking.text
        epilepsy = self.epilepsy.text
        c = [ed, imposter, temper, appointments, concentratetalking, epilepsy]
        gsheet_update = globalshared_data.x + globalshared_data.y + globalshared_data.z + globalshared_data.a + globalshared_data.b + c
        gsheet_update = [float(x) for x in gsheet_update]
        wk_1 = client.open("ADHD App API").worksheet("Data_Input")
        next_row = next_available_row(wk_1)
        wk_1.update(f'A{next_row}:AE{next_row}', [gsheet_update])



#update Diagnosis for prediction - classes seperated by screens to be accessed by the kivy files associated
class Diagnosis(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def diag_on_press(self):
        age = self.age.text
        time = self.time.text
        lead = self.time.text
        decisions = self.decisions.text
        globalshared_diagnosis.x = [age, time, lead, decisions]
                    
class Diagnosis2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def diag_two_on_press(self):
        depression = self.depression.text
        bipolar = self.bipolar.text
        anxiety = self.anxiety.text
        alcohol = self.alcohol.text
        crying = self.crying.text
        globalshared_diagnosis.y = [depression, bipolar, anxiety, alcohol, crying]
                      
class Diagnosis3(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def diag_three_on_press(self):
        headtraumas = self.headtraumas.text
        money = self.money.text
        impatient = self.impatient.text         
        parentsdiagnosed = self.parentsdiagnosed.text
        siblingsdiagnosed = self.siblingsdiagnosed.text
        globalshared_diagnosis.z = [headtraumas, money, impatient, parentsdiagnosed, siblingsdiagnosed]
    
class Diagnosis4(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def diag_four_on_press(self):
        siblingsamount = self.siblingsamount.text
        siblingorder = self.siblingorder.text         
        autism = self.autism.text
        trauma = self.trauma.text
        wfh = self.wfh.text
        globalshared_diagnosis.a = [siblingsamount, siblingorder, autism, trauma, wfh]

class Diagnosis5(Screen):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def diag_five_on_press(self):
        premature = self.premature.text       
        birthweight = self.birthweight.text
        ethnicity = self.ethnicity.text
        speedingticket = self.speedingticket.text
        publicoverwhelmed = self.publicoverwhelmed.text
        globalshared_diagnosis.b = [premature, birthweight, ethnicity, speedingticket, publicoverwhelmed]

class Diagnosis_Submit(Screen): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
    def diag_submit_on_press(self):
        ed = self.ed.text
        imposter = self.imposter.text
        temper = self.temper.text
        appointments = self.appointments.text        
        concentratetalking = self.concentratetalking.text
        epilepsy = self.epilepsy.text
        c = [ed, imposter, temper, appointments, concentratetalking, epilepsy]
        gsheet_update = globalshared_data.x + globalshared_data.y + globalshared_data.z + globalshared_data.a + globalshared_data.b + c
        gsheet_update = [float(x) for x in gsheet_update]
        wk_2 = client.open("ADHD App API").worksheet("Diagnosis_Input")
        next_row = next_available_row(wk_2)
        wk_2.update(f'A{next_row}:AE{next_row}', [gsheet_update])
