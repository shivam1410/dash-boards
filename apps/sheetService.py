from auth.sheetAuth import getSheetService
from flask_caching import Cache
import pandas as pd
from index import app

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



# def query_data():
#     # This could be an expensive data querying step
#     df = getSheets()
#     return df.to_json(date_format='iso', orient='split')

# def dataframe():
#     return pd.read_json(query_data(), orient='split')
