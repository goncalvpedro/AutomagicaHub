class Asset:

    def __init__(self, ticker, buying_date, paid_price, quantity, in_possession):
        self.ticker = ticker
        self.buying_date = buying_date
        self.paid_price = paid_price
        self.quantity = quantity
        self.short_name, self.type, self.current_price, self.investment_value, self.dividend_received, self.in_possession = self.from_yahoo(self.ticker)
        self.in_possession = bool(in_possession)
    
    def __str__(self):
        return f'Asset {self.name} created successfully'
    
    def asset_info(self):
        return f'Ticker: {self.ticker}, Short Name: {self.short_name}, Buying Date: {self.buying_date}, Paid Price: {self.paid_price}, Quantity: {self.quantity}, Type: {self.type},Current Price: {self.current_price}, Investment Value: {self.investment_value}, Dividend Received: {self.dividend_received}, In Possession: {self.in_possession}'

    @classmethod
    def from_yahoo(cls, ticker):
        import yfinance as yf

        if type(ticker) == str:
            ticker = ticker.upper()
        else:
            return 'Ticker must be a string'
        
        ticker_object = yf.Ticker(ticker)

        print(ticker_object.info['shortName'])
        shortName = ticker_object.info['shortName']
        asset_type = ticker_object.info['quoteType']
        asset_current_price = ticker_object.info['previousClose']
        asset_investment_value = '' # function to calculate quantity times current price
        asset_dividend_received = '' # function to get dividends from the buying date and sum


        return cls(shortName, asset_type, asset_current_price, asset_investment_value, asset_dividend_received)
    
# Instanciando a classe
asset = Asset('FII IRIDIUM CI', '2021-05-01', 96, 28, True)

print(asset)
