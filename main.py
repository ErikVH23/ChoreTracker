#Project: Chore Tracker
#Version: 0.1
#Author: Erik Van Horn
#Last Updated: 02/3/2021

from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

import requests



SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '13UtdWJcijKtvmfDDRcNU2M-JKJ3NoUJHv2DCbaBXQv0'
RANGE = 'Sheet1!B3:B9&Sheet1D3:D9'

with open('credentials.json') as f:
    c = json.load(f)

KEY = json.dumps(c)
print(KEY)

URL = 'https://sheets.googleapis.com/v4/spreadsheets/'+SPREADSHEET_ID+'/values:batchGet?ranges=Sheet1!B:B&ranges=Sheet1!D:D&valueRenderOption=UNFORMATTED_VALUES?majorDimension=COLUMNS/key'+KEY

def main():

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle','wb') as token:

            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    #result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    #value = result.get('values',[])

    r = requests.get(URL)

    print(r.text)


if __name__ == '__main__':
    main()
