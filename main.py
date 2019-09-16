import superSimpleStock

stock= superSimpleStock.Stock('test/sample_data.csv')

print('Cleaned dataFrame created from csv file : \n{} '.format(stock.gbce_data))

# calculate_dividend_yield
print('i: Dividend for Stock: ')
print('TEA : {} '.format(stock.calculate_dividend_yield(stock='TEA', ticker_price=3)))
print('POP : {} '.format(stock.calculate_dividend_yield(stock='POP', ticker_price=3)))
print('GIN : {} '.format(stock.calculate_dividend_yield(stock='GIN', ticker_price=3)))

# calculate_pe_ratio
print('ii: P/E Ratio for Stock:  ')
print('TEA : {} '.format(stock.calculate_pe_ratio(stock='TEA', ticker_price=2)))
print('POP : {} '.format(stock.calculate_pe_ratio(stock='POP', ticker_price=3)))
print('GIN : {} '.format(stock.calculate_pe_ratio(stock='GIN', ticker_price=3)))

# record_trade
stock.record_trade(stock='POP', quantity=10, sold=True, price=5)
stock.record_trade(stock='POP', quantity=11, sold=True, price=6)
stock.record_trade(stock='POP', quantity=12, sold=False, price=7)
stock.record_trade(stock='TEA', quantity=1, sold=True, price=7)
print('iii: Record Trades: \n{} '.format(stock.trade))

# calculate_stock_price
print('iv: Stock Price:  {} '.format(stock.calculate_stock_price('POP')))

# calculate_stock_price
print('b: GBCE All Share Index:   {} '.format(stock.calculate_all_share_index()))

