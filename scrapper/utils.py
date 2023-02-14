from datetime import datetime
from dateutil.relativedelta import relativedelta

def process_date(date: str):
    current_date = datetime.today()
    date = date.split()

    if date[1] == 'jam':
        past_date = current_date - relativedelta(hours=int(date[0]))
    elif date[1] == 'hari':
        past_date = current_date - relativedelta(days=int(date[0]))
    elif date[1] == 'minggu':
        past_date = current_date - relativedelta(weeks=int(date[0]))
    elif date[1] == 'bulan':
        past_date = current_date - relativedelta(months=int(date[0]))
    elif date[1] == 'tahun':
        past_date = current_date - relativedelta(years=int(date[0]))
    
    if date[0] == 'setahun':
        past_date = current_date - relativedelta(years=1)
    elif date[0] == 'sebulan':
        past_date = current_date - relativedelta(months=1)
    elif date[0] == 'seminggu':
        past_date = current_date - relativedelta(weeks=1)

    return str(past_date)[:19]