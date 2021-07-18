import requests
import traceback
import datetime
import json
import logging
import sys
import ssl
import urllib.request
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# current_date = datetime.datetime.now()
#
# root = logging.getLogger()
# root.setLevel(logging.DEBUG)
#
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)

logger = logging.Logger('WeTransfer', logging.INFO)
def pprint(msg, level=logging.INFO, *args, **kwargs):
    logger.log(level, msg, *args, **kwargs)


def prices_data(start, end):
    base_url = 'https://api.coindesk.com'
    endpoint = f'/v1/bpi/historical/close.json?start={start}&end={end}'
    try:
        pprint(f'{base_url}{endpoint}')
        pprint('Retrieving data from 1C')
        response = requests.get(url=f'{base_url}{endpoint}')
    except requests.exceptions.HTTPError:
        traceback.print_exc()
    else:
        if response.status_code not in [200, 202]:
            pprint(f'code: {response.status_code} url: {base_url}{endpoint}')
            return
        parsed = json.loads(response.text)
        return parsed['bpi']


def exrate_data(start, end):
    gcontext = ssl.SSLContext()
    url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/usd.xml'
    response = urllib.request.urlopen(url, context=gcontext).read()
    tree = ET.fromstring(response)

    result = {}
    relevant = False
    for x in tree[1][1]:
        if not relevant:
            relevant = x.attrib.get('TIME_PERIOD') == datetime.datetime.strftime(start, '%Y-%m-%d')

        if relevant:
            result[x.attrib.get('TIME_PERIOD')] = x.attrib.get('OBS_VALUE')
            relevant = x.attrib.get('TIME_PERIOD') != datetime.datetime.strftime(end, '%Y-%m-%d')

    return result


def dates_threshold():
    start_dt = datetime.date(datetime.date.today().year - 1, datetime.date.today().month, datetime.date.today().day)
    end_dt = datetime.date.today()

    return start_dt, end_dt


def dates_scope_df(start, end):
    dates = [x.strftime('%Y-%m-%d') for x in pd.date_range(start, end - datetime.timedelta(days=1), freq='D')]
    return pd.DataFrame(
        {'dttm': dates},
        columns=['dttm', 'exchange_rate', 'usd_price', 'eur_price', 'week_rolling_avg']
    )


def add_exrate(dates, start, end):
    ex_rate_data = exrate_data(start, end)
    dates['exchange_rate'] = dates['dttm'].map(ex_rate_data)
    return dates

def add_usd_price(dates, start, end):
    usd_prices = prices_data(start, end)
    dates['usd_price'] = dates['dttm'].map(usd_prices)
    return dates

if __name__ == '__main__':
    # Build dates scope
    start, end = dates_threshold()
    df = dates_scope_df(start, end)

    # A exchange rates on a date
    df = add_exrate(df, start, end)

    # Add coin usd price
    df = add_usd_price(df, start, end)
    print('lol')
    # fill weekends
    df.fillna(method='ffill', inplace=True)

    # Add eur price
    df['eur_price'] = df['usd_price'].astype('float') * df['exchange_rate'].astype('float')

    df['week_rolling_avg'] = df['eur_price'].rolling(7, min_periods=7).mean()
    print(df)

    file_name = 'price_index_data.csv'
    df.to_csv(file_name, columns=['dttm', 'usd_price', 'eur_price', 'week_rolling_avg'], index=False)
    df.plot(x='dttm', y='week_rolling_avg')
    plt.show()
    plt.close("all")
