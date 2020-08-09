import numpy as np
import backtrader as bt
import backtrader.feeds as btfeeds
import datetime
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import logging

from data_reader import load_data
from money_management import forex_risk_calculator
from configuration import parameters
from ta.volatility import average_true_range
from backtest_strategy import Backtrader_Strategy
from custom_strategy import TestStrategy_SMA_Basic
from my_strategy import custom_strategy_example

class backtesting(object):
	def __init__(self, config):
		print('Initiating backtesting')
		self.config = config
		self.data_path = config['data_path']
		self.mode = config['trading_mode']
		self.data_loader = load_data(self.config)
		self.all_symbols, self.all_data = self.data_loader.load_all_data()
		self.symbol_data = self.data_loader.load_symbol(self.all_data, self.all_symbols, config['target_symbol'])

		self.config['base_target_symbol'] = self.config['account_base'] + '_' + self.config['target_symbol'][4:]
		print(self.config['base_target_symbol'])

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


	def trade_config(self, data, atr):

		base = self.config['account_base']
		target = self.config['target_symbol']
		order = self.config['order']
		balance = self.config['account_balance']
		risk = self.config['risk_per_trade']

		if self.mode == 'forex':
			pair = config['target_symbol']
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
		
		#data = self.load_symbol(self.config['target_symbol'])

		# Create a cerebro entity
		bro = bt.Cerebro()

		# Add a strategy
		bro.addstrategy(custom_strategy_example)

		# Add logging writer 
		random_number = str(np.random.randint(1000))
		bro.addwriter(bt.WriterFile, out = self.config['output_path'] + 'results' + random_number + '.csv', csv = True)

		#Sizer for now TODO remove and implement money management
		bro.addsizer(bt.sizers.PercentSizerInt, percents = 2)
		
		# Set our desired cash start
		bro.broker.setcash(self.config['starting_balance'])

		# transform the dataframe into a datafeed
		data = bt.feeds.PandasData(dataname=self.symbol_data)

		# Add the Data Feed to Cerebro
		bro.adddata(data)

		# Set the commission
		bro.broker.setcommission(commission= self.config['broker_commission'])
		
		# Print out the starting conditions
		print(f'Starting Portfolio Value: {bro.broker.getvalue()}')

		# Run over everything
		bro.run()

		print(f'Final Portfolio Value: {bro.broker.getvalue()}')

		if self.config['plot'] == True:
			bro.plot()

