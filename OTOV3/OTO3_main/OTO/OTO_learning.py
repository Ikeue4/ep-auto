import os
import configparser
from datetime import datetime

def set_data_persistent(name, errors, times):
    data_path = os.path.join(os.path.dirname(__file__), 'data.ini')

    data = configparser.ConfigParser()
    data.read(data_path)

    percentage = (times - errors) / times * 100

    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    info_date = currentDay, currentMonth, currentYear

    try:
        data.set(name, 'day', str(currentDay))
        data.set(name, 'month', str(currentMonth))
        data.set(name, 'year', str(currentYear))
        data.set(name, 'accuracy', str(percentage))
        with open(data_path, 'w') as dataf:
            data.write(dataf)
        
    except:
        data.add_section(name)
        data.set(name, 'day', str(currentDay))
        data.set(name, 'month', str(currentMonth))
        data.set(name, 'year', str(currentYear))
        with open(data_path, 'w') as dataf:
            data.write(dataf)
            
def get_data_persistent(name):
    data_path = os.path.join(os.path.dirname(__file__), 'data.ini')

    data = configparser.ConfigParser()
    data.read(data_path)

    day = data.get(name, 'day')
    month = data.get(name, 'month')
    year = data.get(name, 'year')
    percentage = data.get(name, 'accuracy')
    
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    
    from_date = datetime(int(year), int(month), int(day))
    current_date = datetime(currentYear, currentMonth, currentDay)
    difference = current_date - from_date
    
    difference_in_days = difference.days
    
    return difference_in_days, percentage