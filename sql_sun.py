from __future__ import print_function
from datetime import datetime
import pickle
import os.path
import datetime
import pyodbc
import time
import threading
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = 'xxxx'
SAMPLE_RANGE_NAME = 'Sheet1!a1:I1000000'


def getresults():
    try:
        connection = pyodbc.connect('Driver={SQL Server};'
                              'Server=.\xxxxx;'
                              'Database=xxxxx;'
                              'Trusted_Connection=yes;')

        cursor = connection.cursor()
        cursor.execute(
            """ SELECT *  FROM table_name WHERE FLAG=0 and pmax>0 and voc>0 and Isc>0 and vpm>0 and Ipm>0 and ID not like '%cal%' and ID not like '%CAL%' and ID not like '%KAL%' and ID not like '%kal%' and LEN(ID) between 10 and 15""")
        records = cursor.fetchall()
        return records
        cursor.close()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        # closing database connection.
        connection.close()


def setresults(ID, Date, Time):
    try:
        connection = pyodbc.connect('Driver={SQL Server};'
                                    'Server=.\xxxx;'
                                    'Database=xxxx;'
                                    'Trusted_Connection=yes;')
        cursor = connection.cursor()
        named_params = [ID, Date, Time]
        cursor.execute('Update Sun_Results  set FLAG=1 WHERE FLAG=0 and ID=? and Test_date=? and test_TIME=?',named_params)
        cursor.close()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        # closing database connection.
        connection.commit()
        connection.close()


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # oracle'dan gelen sonucu bir değişkene atıyorum, döngü ile gelen her satır için gsheet'e yazıyorum
    query_results = getresults()
    seperator='-'
    for results in query_results:
        ## burada tarihi istenen formata çeviriyoruz.
        datepart=results[4].split(seperator)
        lastdate=datepart[1]+seperator+datepart[2]+seperator+datepart[0]        
        values = [
           #[results[3], results[4].strftime('%m-%d-%Y'), results[5], results[7], results[9], results[10], results[11],
            [results[3],lastdate ,results[5], results[7], results[9], results[10], results[11],
             
             results[12], results[-3]]
        ]
        spreadsheet_body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED", body=spreadsheet_body).execute()
        print('{0} cells appended.'.format(result \
                                           .get('updates') \
                                           .get('updatedCells')))

        print(values)
        time.sleep(1)
        setresults(results[3], results[4], results[5])


if __name__ == '__main__':
    main()

##    timer = threading.Timer(5.0, main)
##    timer.start()
##    timer1 = threading.Timer(5.0,setresults)
##    timer1.start()

