import gspread

from oauth2client.service_account import ServiceAccountCredentials


def gSheets():
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('cogs/utils/config.json', scope)
            gc = gspread.authorize(credentials)        
            if credentials.access_token_expired:
                gc.login()
            gSheets = gc.open('Horizon Leaderboards')  
            return gSheets
        except Exception as e:
            print(e)