import datetime
import requests
import fake_useragent

class Intervals:
    Daily   = '1d'
    Weekly  = '1wk'
    Monthly = '1mo'
    
__session: requests.Session = None

def set_session(session: requests.Session):
    global __session
    __session = session

def get_stock_history(
    ticker: str, 
    from_date: datetime.datetime, 
    to_date: datetime.datetime = datetime.datetime.now(), 
    interval: str = Intervals.Daily):
    '''
    Parameters
    ----------
    ticker : The symbol of the stock to get the history of.
    
    from_date : The date the history starts at.
    
    to_date : The date the history stops at. Today by default.
    
    interval: '1d' (default), '1wk', or '1mo'. These strings are contained in `Intervals`.
    
    session : Optional parameter if you want to pass in a `requests.Session`.
    Otherwise `requests.get` is used.

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    HTTPError
        when a key error
    OtherError
        when an other error
    '''
    global __session
    
    # Clean up parameters.
    getter = __session.get if __session is not None else requests.get
    to_date = to_date if to_date is not None else datetime.datetime.now()
    
    # Get timestamps.
    period1 = int(from_date.timestamp())
    period2 = int(to_date.timestamp())
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}'
    
    # Make request.
    response = getter(
        url=url,
        params={
            'period1': period1,
            'period2': period2,
            'interval': interval,
            'events': 'history',
            'includeAdjustedClose': True
            },
        headers={
            'User-Agent': fake_useragent.FakeUserAgent().random
            },
        stream=True)
    response.raise_for_status()
    
    # Read csv column labels.
    lines = response.iter_lines()
    columns = next(lines).decode().split(',')
    n_columns = len(columns)
    
    # Convert csv to list of dicts.
    history = []
    for line in lines:
        values = line.decode().split(',')
        item = {
            columns[i]: values[i] for i in range(n_columns)
        }
        history.append(item)
        
    return history
