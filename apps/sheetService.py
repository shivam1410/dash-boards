from auth.sheetAuth import getSheetService
from flask_caching import Cache
import pandas as pd
from index import app
from datetime import datetime, date, timedelta

SAMPLE_SPREADSHEET_ID = '18n86FnoHeqY1HCvaSHPXf2vbzjDZmw2gcO1Iv2XeD0Y'
SAMPLE_RANGE_NAME = 'Form!A2:E'
columns=['Date', 'Start Time', 'End Time', 'Activity', 'Category']
sheetData = pd.DataFrame([], columns=columns);

cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DIR': 'data'
})


TIMEOUT = 60

@cache.memoize(timeout=TIMEOUT)
def getSheets():
    service = getSheetService()
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    print("Size of data fetched from Sheet is : ")
    print(len(values))
    global sheetData 
    sheetData= pd.DataFrame(values, columns=columns);
    return sheetData

def getSheetData():
    return getSheets()

def get_ranged_sheet_data(startdate, enddate):
    df = getSheetData();
    df = df[(pd.to_datetime(df.Date)>=datetime.strptime(startdate, '%Y-%m-%d'))&(pd.to_datetime(df.Date)<=datetime.strptime(enddate,'%Y-%m-%d'))]
    return df;
