"""
    The Stock object is constructed from a csv file of given stock data. See
    sample_data.csv for an example and superSimpleStockTest.py for test cases.
"""

import pandas
import re
import math
import datetime
import dateutil


class Stock:

    def __init__(self, csv_file):
        self.gbce_data = self._read_gbce_stock_data(csv_file)
        self.trade = pandas.DataFrame({'Stock_Symbol': [], 'timestamp': [], 'quantity': [], 'sold': [], 'price': []})

    # i. Calculate the dividend yield
    def calculate_dividend_yield(self, stock, ticker_price):
        dstock = self.gbce_data[self.gbce_data['Stock_Symbol'] == stock]
        if len(dstock['Type']) != 1:
            raise StockException('Too many or no values for\n%s' % stock)

        if list(dstock['Type'])[0] == 'Common':
            return list(dstock['Last_Dividend'])[0] / ticker_price
        elif list(dstock['Type'])[0] == 'Preferred':
            return (list(dstock['Fixed_Dividend'])[0] * list(dstock['Par_Value'])[0]) / ticker_price
        else:
            raise Exception('Unexpected stock type:\n%s' % dstock['Type'])

    # ii. Calculate the P/E Ratio
    def calculate_pe_ratio(self, stock, ticker_price):
        dividend = self.calculate_dividend_yield(stock, ticker_price)
        if dividend == 0:
            return float('nan')
        return ticker_price / dividend

    # iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and price
    # Record the trade of the given stock and append it to the trade dataFrame.
    # sold: boolean. If True, the stock has been sold. If False, it has been bought
    def record_trade(self, stock, quantity, sold, price):
        if stock not in set(self.gbce_data['Stock_Symbol']):
            raise StockException('Unknown stock: %s' % stock)

        trade = {'Stock_Symbol': stock,
                 'timestamp': datetime.datetime.now().isoformat(),
                 'quantity': quantity,
                 'sold': sold,
                 'price': price}
        self.trade = self.trade.append(trade, ignore_index=True)

    # iii. Calculate Stock Price based on trades recorded in past 15 minutes
    # Return NaN if no transactions are available.
    def calculate_stock_price(self, stock, last_minutes=15):
        time = datetime.datetime.now() - datetime.timedelta(minutes=last_minutes)

        if len(self.trade) == 0:
            return float('nan')

        tstock = self.trade[self.trade['Stock_Symbol'] == stock]
        if len(tstock) == 0:
            return float('nan')

        last_trades = [dateutil.parser.parse(x) > time for x in list(tstock['timestamp'])]

        tstock = tstock[last_trades]
        if len(tstock) == 0:
            return float('nan')

        # This includes both sold and bought trades
        return sum(tstock['price'] * tstock['quantity']) / sum(tstock['quantity'])

    # b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
    def calculate_all_share_index(self):
        if len(self.trade) == 0:
            return float('nan')
        all_share_index = 1
        n = 0
        for p in list(self.trade['price']):
            all_share_index *= p
            n += 1
        return all_share_index ** (1 / n)

    # read data from CSV
    def _read_gbce_stock_data(self, csv_file):
        # Read the given csv file and return a cleaned dataFrame
        gbce_data = pandas.read_csv(csv_file)
        fixed_dividend = []
        for x in gbce_data['Fixed_Dividend']:
            # Convert the strings 'd%' to numeric unless the cell value is NaN.
            if type(x) == float and math.isnan(x):
                pass
            else:
                try:
                    x = float(re.sub('%', '', x)) / 100
                except:
                    raise ('Cannot convert %s to numeric' % x)
            fixed_dividend.append(x)
        gbce_data['Fixed_Dividend'] = fixed_dividend
        return gbce_data


class StockException(Exception):
    pass
