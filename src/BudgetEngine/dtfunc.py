from datetime import datetime as dt
from datetime import timedelta
import calendar as cal

#defining verbose function
verboseON=0

def verbose(object):
    if verboseON == 1:
        print(object)
    elif verboseON == 0:
        pass


def dtfunc(period,component,fmt='dt'):
    """compiles various common date strings for use

    Args:
        period (str): Options: 
            [today],
                component (str): Options:
                    ['fulldate'],
                    ['day'],
                    ['month'],
                    ['year']
            [current]
                component (str): Options: 
                    ['last_day_month'],
                    ['last_date_month'],
                    ['first_day_month']
        fmt(str): Options:
            ['dt'],
            ['str']
    """
    if period=="today":
        if component=="fulldate":
            dateout = dt.datetime(dt.datetime.today().year, dt.datetime.today().month, dt.datetime.today().day)
        if component=="day":
            dateout = dt.datetime.today().day
        if component=="month":
            dateout = dt.datetime.today().month
        if component=="year":
            dateout = dt.datetime.today().year
    
    if period=="current":
        if component=="last_day_month":
            dateout = cal.monthrange(dtfunc('current','year'),dtfunc('current','month'))[1]
        if component=="last_date_month":
            dateout = dt.datetime(dtfunc('current','year'),dtfunc('current','month'),dtfunc('current','last_day_month'))
        if component=="first_date_month":
            dateout = dt.datetime(dtfunc('current','year'),dtfunc('current','month'),1)
    
    if fmt=='str':
        return dateout.strftime('%Y-%m-%d')
    if fmt=='int':
        return int(dateout.strftime('%Y%m%d'))
    else:
        return dt.datetime.strptime(dateout.strftime('%Y-%m-%d'), '%Y-%m-%d')

def convDate(inputdate: str):
    """This function takes an input of a string and formats as a datetime value and strips the time

    Args:
        inputdate (str): input date string

    Returns:
        _type_: date as datetime object
    """
    x = dt.strptime(inputdate,"%Y-%M-%d").date
    return x

def txIterate(frequency: str, inputdate: dt):
    """Given a frequency and input date, this function will calculate the next date based on the frequency

    Args:
        frequency (str): 
            "daily",
            "weekly",
            "biweekly",
            "monthly",
            "quarterly",
            "yearly"
        inputdate (dt.date): input date as datetime object

    Returns:
        dt.date: new date as datetime object
    """
    startdate = inputdate
    if frequency == "daily": delta = timedelta(days=1)
    if frequency == 'weekly': delta = timedelta(weeks=1)
    if frequency == 'biweekly': delta = timedelta(weeks=2)
    if frequency == 'monthly': delta = timedelta(weeks=4)
    if frequency == 'quarterly': delta = timedelta(weeks=12)
    if frequency == 'yearly': delta = timedelta(years=1)
    if isinstance(startdate,str):
        startdate=convDate(startdate)
    x = startdate + delta
    return x

