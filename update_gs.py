#importing dependencies for our kv screen information
from kivy.lang import Builder

#importing gsheets dependencies
import os
import sys
import gspread
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2 import service_account
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.textinput import TextInput
import pygsheets
import numpy as np
import csv


#authorizaiton to edit
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/jacquelenarz/Downloads/client_secret.json', scope)
client = gspread.authorize(creds)

#open gsheets
sh = client.open('ADHD App API')


#update Data for testing and training
class Data_Input():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('data.kv')
        self.np = []
    def submit(self):
        self.age_data = self.ids.age_data.text
        self.adhd_data = self.ids.adhd_data.text
        self.time_data = self.ids.time_data.text
        self.lead_data = self.ids.lead_data.text
        self.decisions_data = self.ids.decisions_data.text
        self.depression_data = self.ids.depression_data.text
        self.bipolar_data = self.ids.bipolar_data.text
        self.anxiety_data = self.ids.anxiety_data.text
        self.alcohol_data = self.ids.alcohol_data.text
        self.crying_data = self.ids.crying_data.text
        self.headtraumas_data = self.ids.headtraumas_data.text
        self.money_data = self.ids.money_data.text
        self.impatient_data = self.ids.impatient_data.text         
        self.parentsdiagnosed_data = self.ids.parentsdiagnosed_data.text
        self.siblingsdiagnosed_data = self.ids.siblingsdiagnosed_data.text
        self.siblingsamount_data = self.ids.siblingsamount_data.text
        self.siblingorder_data = self.ids.siblingorder_data.text         
        self.autism_data = self.ids.autism_data.text
        self.trauma_data = self.ids.trauma_data.text
        self.wfh_data = self.ids.wfh_data.text
        self.premature_data = self.ids.premature_data.text         
        self.birthweight_data = self.ids.birthweight_data.text
        self.ethnicity_data = self.ids.ethnicity_data.text
        self.speedingticket_data = self.ids.speedingticket_data.text
        self.publicoverwhelmed_data = self.ids.publicoverwhelmed_data.text
        self.ed_data = self.ids.ed_data.text
        self.imposter_data = self.ids.imposter_data.text
        self.temper_data = self.ids.temper_data.text   
        self.appointments_data = self.ids.appointments_data.text         
        self.concentratetalking_data = self.ids.concentratetalking_data.text
        self.epilepsy_data = self.ids.epilepsy_data.text
        self.np = [self.age_data, self.adhd_data, self.time_data, self.lead_data, self.decisions_data, self.depression_data,	self.bipolar_data,	self.anxiety_data,	self.alcohol_data,	self.crying_data,	self.headtraumas_data,	self.money_data,	self.impatient_data, self.parentsdiagnosed_data, self.siblingsdiagnosed_data,	self.siblingsamount_data,	self.siblingorder_data,	self.autism_data, self.trauma_data,	self.wfh_data,	self.premature_data, self.birthweight_data,	self.ethnicity_data, self.speedingticket_data,self.publicoverwhelmed_data,	self.ed_data,	self.imposter_data,	self.temper_data,	self.appointments_data,	self.concentratetalking_data, self.epilepsy_data]
        #appending data_input google sheets
        sh = client.open("ADHD App API").get_worksheet(0)


#insert Diagnosis data to the tensorflow model
class Diagnosis_Input():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('diagnosis.kv')
        self.np = []
    def submit(self):
        self.age_diagnosis = self.ids.age_diagnosis.text
        self.time_diagnosis = self.ids.time_diagnosis.text
        self.lead_diagnosis = self.ids.lead_diagnosis.text
        self.decisions_diagnosis = self.ids.decisions_diagnosis.text
        self.depression_diagnosis = self.ids.depression_diagnosis.text
        self.bipolar_diagnosis = self.ids.bipolar_diagnosis.text
        self.anxiety_diagnosis = self.ids.anxiety_diagnosis.text
        self.alcohol_diagnosis = self.ids.alcohol_diagnosis.text
        self.crying_diagnosis = self.ids.crying_diagnosis.text
        self.headtraumas_diagnosis = self.ids.headtraumas_diagnosis.text
        self.money_diagnosis = self.ids.money_diagnosis.text
        self.impatient_diagnosis = self.ids.impatient_diagnosis.text         
        self.parentsdiagnosed_diagnosis = self.ids.parentsdiagnosed_diagnosis.text
        self.siblingsdiagnosed_diagnosis = self.ids.siblingsdiagnosed_diagnosis.text
        self.siblingsamount_diagnosis = self.ids.siblingsamount_diagnosis.text
        self.siblingorder_diagnosis = self.ids.siblingorder_diagnosis.text         
        self.autism_diagnosis = self.ids.autism_diagnosis.text
        self.trauma_diagnosis = self.ids.trauma_diagnosis.text
        self.wfh_diagnosis = self.ids.wfh_diagnosis.text
        self.premature_diagnosis = self.ids.premature_diagnosis.text         
        self.birthweight_diagnosis = self.ids.birthweight_diagnosis.text
        self.ethnicity_diagnosis = self.ids.ethnicity_diagnosis.text
        self.speedingticket_diagnosis = self.ids.speedingticket_diagnosis.text
        self.publicoverwhelmed_diagnosis = self.ids.publicoverwhelmed_diagnosis.text
        self.ed_diagnosis = self.ids.ed_diagnosis.text
        self.imposter_diagnosis = self.ids.imposter_diagnosis.text
        self.temper_diagnosis = self.ids.temper_diagnosis.text   
        self.appointments_diagnosis = self.ids.appointments_diagnosis.text         
        self.concentratetalking_diagnosis = self.ids.concentratetalking_diagnosis.text
        self.epilepsy_diagnosis = self.ids.epilepsy_diagnosis.text
        self.np = [self.age_diagnosis, self.time_diagnosis, self.lead_diagnosis, self.decisions_diagnosis, self.depression_diagnosis,	self.bipolar_diagnosis,	self.anxiety_diagnosis,	self.alcohol_diagnosis,	self.crying_diagnosis,	self.headtraumas_diagnosis,	self.money_diagnosis,	self.impatient_diagnosis, self.parentsdiagnosed_diagnosis, self.siblingsdiagnosed_diagnosis,	self.siblingsamount_diagnosis,	self.siblingorder_diagnosis,	self.autism_diagnosis, self.trauma_diagnosis,	self.wfh_diagnosis,	self.premature_diagnosis, self.birthweight_diagnosis,	self.ethnicity_diagnosis, self.speedingticket_diagnosis,self.publicoverwhelmed_diagnosis,	self.ed_diagnosis,	self.imposter_diagnosis,	self.temper_diagnosis,	self.appointments_diagnosis,	self.concentratetalking_diagnosis, self.epilepsy_diagnosis]
        #appending data_input google sheets
        sh = client.open("ADHD App API").get_worksheet(1)
