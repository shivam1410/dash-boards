from auth.sheetAuth import getSheetService
import pandas as pd
SAMPLE_SPREADSHEET_ID = '18n86FnoHeqY1HCvaSHPXf2vbzjDZmw2gcO1Iv2XeD0Y'
SAMPLE_RANGE_NAME = 'Form!A2:E'
columns=['Date', 'Start Time', 'End Time', 'Activity', 'Category']

sheetData = pd.DataFrame([], columns=columns);

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
    return sheetData;

def getSheetData():
    return sheetData;

