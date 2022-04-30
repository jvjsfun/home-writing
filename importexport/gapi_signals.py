from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
    # 'https://www.googleapis.com/auth/spreadsheets'
]


def get_credentials():
    return ServiceAccountCredentials.from_json_keyfile_name(
        'Test-c603e7f2b9c5.json', SCOPE)
