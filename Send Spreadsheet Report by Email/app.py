import pandas as pd
import yfinance as yf
import requests_cache

from datetime import datetime

import send_email

from pathlib import Path

import warnings
warnings.filterwarnings('ignore')


PROJECT_FOLDER = Path(__file__).parent
DATA_FOLDER = PROJECT_FOLDER / 'data'


months = {
    '01': 'Janeiro',
    '02': 'Fevereiro',
    '03': 'Março',
    '04': 'Abril',
    '05': 'Maio',
    '06': 'Junho',
    '07': 'Julho',
    '08': 'Agosto',
    '09': 'Setembro',
    '10': 'Outubro',
    '11': 'Novembro',
    '12': 'Dezembro'
}

session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'my-program/1.0'

# Get csv files exported in the last execution
def get_data():
    old_portfolio = pd.read_csv(DATA_FOLDER / 'portfolio.csv', header = 0)
    dividends = pd.read_csv(DATA_FOLDER / 'dividends.csv', header = 0)
    dividends.columns = ['ticker', 'date', 'qtd', 'dividend']

    return old_portfolio, dividends

# Update assets with most recent price
def updating_price(portfolio):
    updated_prices = []
    for asset in portfolio.ticker:
        asset_object = yf.Ticker(asset)
        asset_price = asset_object.info['previousClose']
        updated_prices.append(asset_price)
    portfolio['current_price'] = updated_prices
    portfolio['invested_value'] = portfolio.qtd * portfolio.paid_price
    portfolio['current_value'] = portfolio.qtd * portfolio.current_price

    return portfolio

# Updating dividends data base with every dividend received in the current month
def updating_dividends(portfolio, dividends):

    for asset in portfolio.ticker:

        new_row = {}

        asset_object = yf.Ticker(asset)
        asset_dividends = asset_object.dividends

        asset_dividends.index = pd.to_datetime(asset_dividends.index)
        current_month = datetime.today().strftime('%Y-%m')

        asset_dividends = asset_dividends[asset_dividends.index.strftime('%Y-%m') == current_month]

        try:
            new_row = {
            'ticker': asset,
            'date' : asset_dividends.index.strftime('%Y-%m-%d')[0],
            'qtd': portfolio.loc[portfolio['ticker'] == asset, 'qtd'].values[0],
            'dividend' : asset_dividends.values[0], 
        }

        except:
            f'{asset} não distribiu dividendos esse mês.'

        new_row = pd.DataFrame(new_row, index=[0])

        if new_row.empty:
            continue
        else:
            dividends = pd.concat([dividends, new_row], ignore_index=True)
            dividends = dividends.reset_index(drop=True)

        dividends['total_received'] = dividends.qtd * dividends.dividend

    return dividends

# Export 'Dividends' and 'Portfolio' dataframes with current month information
def exporting_data():
    portfolio.to_csv(DATA_FOLDER / 'portfolio.csv', index=False)
    dividends.to_csv(DATA_FOLDER / 'dividends.csv', index=False)


# Function calling
portfolio, dividends = get_data()

updated_portfolio = updating_price(portfolio)

updated_dividends = updating_dividends(portfolio, dividends)

# Dataframe manipulation
updated_dividends['ticker'] = updated_dividends.ticker.str.strip()
updated_dividends['date'] = updated_dividends.date.str.strip().astype('datetime64[ns]')
grouped_dividends = updated_dividends.groupby('ticker').total_received.sum()


# Getting the desired KPI's
# 1. Total amount of dividends received in the current month

# 2. Portfolio current value

# 3. Portfolio total return

# 4. Top 3 assets

# 5. Bottom 3 assets


# Second level function calling


# Printing the KPI's

print(f'Dividendos recebidos no último mês:\n{''}')
print(f'Valor total recebido no último mês: R${''}')
print(f'Atual composição do portfolio:\n{''}\n')
print(f'Valor total do portfolio: R${''}\n')
print(f'Retorno do portfolio: {''}%')



# Sending the email

from_email = 'pedrogoncalves.ie@gmail.com'
to_email = 'pedrogoncalves.ie@gmail.com'
subject = 'Monthly Investment Report'

body = f'''
        E-mail body
'''


# # send_email.send_email(from_email, to_email, subject, body)