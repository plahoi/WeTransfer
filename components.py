import requests
import traceback
import datetime
import json
import streamlit as st
import urllib.request
import pandas as pd
import xml.etree.ElementTree as ET


@st.cache
def prices_data(start, end):
    base_url = 'https://api.coindesk.com'
    endpoint = f'/v1/bpi/historical/close.json?start={start}&end={end}'
    print(f'{base_url}{endpoint}')
    try:
        response = requests.get(url=f'{base_url}{endpoint}')
    except requests.exceptions.HTTPError:
        traceback.print_exc()
    else:
        if response.status_code not in [200, 202]:
            return
        parsed = json.loads(response.text)
        return parsed['bpi']


def load_exchange_rate_data():
    url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/usd.xml'
    response = urllib.request.urlopen(url).read()
    tree = ET.fromstring(response)

    df = pd.DataFrame((x.attrib for x in tree[1][1]), columns=['TIME_PERIOD','OBS_VALUE'])
    df.set_index('TIME_PERIOD', inplace=True)
    return df


def dates_threshold():
    # Although, the subtraction of a year can be done with dateutil
    start_dt = datetime.date(datetime.date.today().year - 1, datetime.date.today().month, datetime.date.today().day)
    end_dt = datetime.date.today()

    return start_dt, end_dt


def dates_scope_df(start, end):
    # let's get 20 more days in case of holidays / weekends or running average :)
    return pd.date_range(start - datetime.timedelta(days=20), end - datetime.timedelta(days=1), freq='D')


def get_exchange_rate(dates):
    ex_rate_data = load_exchange_rate_data()
    # Full Join of rates and existing dates
    ex_rate_data.index = pd.DatetimeIndex(ex_rate_data.index)
    ex_rate_data = ex_rate_data.reindex(dates, fill_value=0)
    # Fill absent rate data with last known
    ex_rate_data['OBS_VALUE'].replace(to_replace=0, method='ffill', inplace=True)
    ex_rate_data.columns = ['exchange_rate']
    return ex_rate_data


def add_usd_price(df):
    usd_prices = prices_data(df.index[0].date(), df.index[-1].date())
    df['usd_price'] = df.index.map(mapper=(lambda x: usd_prices.get(datetime.datetime.strftime(x, '%Y-%m-%d'))))
    return df


def add_transformations(df):
    # Add eur price
    df['eur_price'] = df['usd_price'].astype('float') * df['exchange_rate'].astype('float')
    df['week_rolling_avg'] = df['eur_price'].rolling(7, min_periods=7).mean()
    return df


# if __name__ == '__main__':
    # Build dates scope
    # start, end = dates_threshold()
    # dates = dates_scope_df(start, end)
    # #
    # # A exchange rates on a date
    # exchange_rate = get_exchange_rate(dates)
    # print(exchange_rate.head())
    #
    # # Add coin usd price
    # df = add_usd_price(exchange_rate)
    # print(df.head())
    # print(df.head(20))
    # df = add_transformations(df)
#     # fill weekends
#     df.fillna(method='ffill', inplace=True)
#
#     # Add eur price
#     df['eur_price'] = df['usd_price'].astype('float') * df['exchange_rate'].astype('float')
#
#     df['week_rolling_avg'] = df['eur_price'].rolling(7, min_periods=7).mean()
#     print(df)
#
#     file_name = 'price_index_data.csv'
#     df.to_csv(file_name, columns=['dttm', 'usd_price', 'eur_price', 'week_rolling_avg'], index=False)
#     df.plot(x='dttm', y='week_rolling_avg')
#     plt.show()
#     plt.close("all")
