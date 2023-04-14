from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Устанавливаем дату, на которую нужны данные
date = datetime.today().strftime('%Y-%m-%d')

# Подключаемся к API
creds = Credentials.from_authorized_user_file('token.pickle', scopes=['https://www.googleapis.com/auth/fitness.activity.read'])
service = build('fitness', 'v1')

# Запрашиваем данные о шагах за указанный день
try:
    steps = service.users().dataSources().datasets(). \
    get(userId='me', dataSourceId='derived:com.google.step_count.delta:com.google.android.gms:estimated_steps', \
        datasetId=date).execute()
except HttpError as error:
    print('An error occurred: %s' % error)
    steps = None

# Если данные об успешном запросе присутствуют, выводим результаты на экран
if steps != None:
    print('Total Steps:', steps['point'][0]['value'][0]['intVal'])
else:
    print('No step data found for the given date')