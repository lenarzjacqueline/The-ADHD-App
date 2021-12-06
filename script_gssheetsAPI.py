import gspread
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build



#setting up our API credentials to read and write
SCOPES = ['https://googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(
    'service_account.json', scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '13iboRDI7pcjsaWriqcwMvOPd8_d883ZeRlJgnZk4Bn8'
service = build('sheets', 'v4', credentials=creds)


#creating the link to the spreadsheet
sa = gspread.service_account(filename='service_account.json')
sh = sa.open('ADHD App API')


#creating the worksheets
wk_1 = sh.worksheet("Login_Info")
wk_2 = sh.worksheet("Data_Info")
wk_3 = sh.worksheet("Diag_Info")
wk_4 = sh.worksheet("Diag_ML_Output")
wk_5 = sh.worksheet("ML_Diag_Combined")
