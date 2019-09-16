"""From the root directory of this repository, execute tests and check results
with:

py -m unittest test.superSimpleStockTest
"""

import unittest
import math
import superSimpleStock
import time


class TestSuperSimpleStock(unittest.TestCase):

    def testCalculateDividendYieldForStock(self):
        stock = superSimpleStock.Stock('sample_data.csv')
        self.assertAlmostEqual(0, stock.calculate_dividend_yield(stock='TEA', ticker_price=2))
        self.assertAlmostEqual(2.667, stock.calculate_dividend_yield(stock='POP', ticker_price=3), places=3)
        self.assertAlmostEqual(0.667, stock.calculate_dividend_yield(stock='GIN', ticker_price=3), places=3)

        self.assertRaises(superSimpleStock.StockException, stock.calculate_dividend_yield, stock='FOOBAR', ticker_price=3)

    def testCalculatePERatioForStock(self):
        stock = superSimpleStock.Stock('sample_data.csv')
        self.assertTrue(math.isnan(stock.calculate_pe_ratio(stock='TEA', ticker_price=2)))
        self.assertAlmostEqual(3 / 2.667, stock.calculate_pe_ratio(stock='POP', ticker_price=3), places=3)

    def testRecordTrade(self):
        stock = superSimpleStock.Stock('sample_data.csv')
        stock.record_trade(stock='POP', quantity=10, sold=True, price=5)
        self.assertEqual(1, len(stock.trade))

        stock.record_trade(stock='TEA', quantity=10, sold=True, price=5)
        self.assertEqual(2, len(stock.trade))

        self.assertRaises(superSimpleStock.StockException, stock.record_trade, stock='FOOBAR', quantity=10, sold=True,
                          price=5)

    def testCalculateStockPrice(self):
        stock = superSimpleStock.Stock('sample_data.csv')

        self.assertTrue(math.isnan(stock.calculate_stock_price('POP')))

        stock.record_trade(stock='POP', quantity=10, sold=True, price=5)
        stock.record_trade(stock='POP', quantity=15, sold=True, price=4)

        self.assertTrue(math.isnan(stock.calculate_stock_price('TEA')))

        stock.record_trade(stock='TEA', quantity=100, sold=True, price=50)
        stock.record_trade(stock='TEA', quantity=150, sold=True, price=40)

        self.assertAlmostEqual(4.4, stock.calculate_stock_price('POP'))
        self.assertAlmostEqual(44.0, stock.calculate_stock_price('TEA'))

        time.sleep(2)
        self.assertTrue(math.isnan(stock.calculate_stock_price('TEA', last_minutes=0.01)))

    def testGetAllShareIndex(self):
        stock = superSimpleStock.Stock('sample_data.csv')

        self.assertTrue(math.isnan(stock.calculate_all_share_index()))

        stock.record_trade(stock='POP', quantity=10, sold=True, price=1)
        stock.record_trade(stock='POP', quantity=15, sold=True, price=2)
        stock.record_trade(stock='TEA', quantity=100, sold=True, price=3)
        stock.record_trade(stock='TEA', quantity=150, sold=True, price=4)

        self.assertAlmostEqual(2.21, stock.calculate_all_share_index(), places=2)


if __name__ == '__main__':
    unittest.main()
