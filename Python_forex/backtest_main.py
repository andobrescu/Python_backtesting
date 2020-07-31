import numpy as np
import backtrader as bt
import backtrader.feeds as btfeeds
import datetime
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import logging

from Load_test import load_forex_data
from money_management import forex_risk_calculator
from config import parameters
from ta.volatility import average_true_range
from backtest_strategy import Backtrader_Strategy
from custom_strategy import TestStrategy_SMA_Basic

class backtesting(object):
	def __init__(self, params):
		print('Initiating backtesting')
		self.params = params
		self.data_path = params['data_path']
		self.mode = params['trading_mode']
		self.load_all_data()
		self.symbol_data = self.load_symbol(params['target_symbol'])

		self.backdrading()

	def load_all_data(self):

		data_loader = load_forex_data(self.data_path)
		
		if self.mode == 'forex':
			self.symbols, self.data_all = data_loader.read_forex_files()
			print('Done loading data')
		else:
			print('I can only do forex at the moment')
		
		return None

	def load_symbol(self, symbol):
		# QUESTION May need an index and not load the whole DF at the time of the trade.

		target_symbol = symbol

		found_symbol = False

		print(self.symbols)
		for i, j in enumerate(self.symbols):
			if target_symbol in j:
				symbol_idx = i
				found_symbol = True
		
		if not found_symbol:
			print('Target symbol cannot be fount in data')
			return
		else:
			print(f'Found symbol at index {symbol_idx}')

		symbol_data = self.data_all[symbol_idx]

		return symbol_data


	def trade_params(self, data, atr):

		base = self.params['account_base']
		target = self.params['target_symbol']
		order = self.params['order']
		balance = self.params['account_balance']
		risk = self.params['risk_per_trade']

		if self.mode == 'forex':
			pair = params['target_symbol']
			counter_currency = pair[4:]
			quote_currency = pair[:3]


			price_df = self.load_symbol(target)
			price = price_df.iloc[-1]
			price = price['Close']


			if base not in pair:
				base_target_pair = [target + '_' + counter_currency]
				base_price_df = self.load_symbol(base_target_pair)
				base_price = base_price_df.iloc[-1]
				base_price = price['Close']
			else:
				base_price = np.copy(price)

		else:
			print('I can only do forex at the moment')
			return
			
		indicator_atr = average_true_range(price_df['High'], price_df['Low'], price_df['Close'], n=14) 
		# may need to specify a dataframe index for trades.

		trade_specs = forex_risk_calculator(self, base, target, order, price, base_price, risk, atr, balance)

		return trade_specs


	def backdrading(self):
		
		#data = self.load_symbol(self.params['target_symbol'])

		# Create a cerebro entity
		bro = bt.Cerebro()

		# Add a strategy
		bro.addstrategy(TestStrategy_SMA_Basic)

		# Add logging writer 
		bro.addwriter(bt.WriterFile, out = self.params['output_path']+'results6.csv', csv = True)

		#Sizer for now TODO remove and implement money management
		bro.addsizer(bt.sizers.FixedSize, stake=3)
		
		# Set our desired cash start
		bro.broker.setcash(self.params['starting_balance'])

		# transform the dataframe into a datafeed
		data = bt.feeds.PandasData(dataname=self.symbol_data)

		# Add the Data Feed to Cerebro
		bro.adddata(data)

		# Set the commission
		bro.broker.setcommission(commission= self.params['broker_commission'])
		
		# Print out the starting conditions
		print(f'Starting Portfolio Value: {bro.broker.getvalue()}')

		# Run over everything
		bro.run()

		print(f'Final Portfolio Value: {bro.broker.getvalue()}')

		#bro.plot()

#configuration  = parameters()
#testing = backtesting(configuration)

#print('done')
