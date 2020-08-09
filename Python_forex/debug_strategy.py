import backtrader as bt
import numpy as np
from configuration import parameters
from backtest_strategy import Backtrader_Strategy
from ta.volatility import average_true_range

class custom_strategy_debug(Backtrader_Strategy):
	# Custom strategy class :
	def __init__(self):
		super().__init__()
		
		self.indicator_params = (('maperiod', 15),)

		base_price_needed = False

		if self.config['trading_mode'] == 'forex':
			if self.config['account_base'] not in self.config['target_symbol']:
				self.config['base_target_symbol'] = self.config['account_base'] + '_' + self.config['target_symbol'][4:]
				self.data_loader = load_data(self.config)
				self.all_symbols, self.all_data = self.data_loader.load_all_data()
				self.base_symbol_data = self.data_loader.load_symbol(self.all_data, self.all_symbols, self.config['base_target_symbol'])
				self.target_symbol_data = self.data_loader.load_symbol(self.all_data, self.all_symbols, self.config['target_symbol'])
				base_price_needed = True
				print('ping pong long')
				

		# Add any indicator here:

		self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.indicator_params.maperiod)

	def next(self):
		# Simply log the closing price of the series from the reference
		self.log('Close, %.4f' % self.dataclose[0])
		
		self.counter += 1
		print(self.counter)
		pair = self.config['target_symbol']

		# Check if an order is pending ... if yes, we cannot send a 2nd one
		if self.order:
			return

		# Check if we are in the market
		if not self.position:

			# Not yet ... we MIGHT BUY if ...
			if self.dataclose[0] > self.sma[0]:

				self.config['order'] = 'buy' 
				if base_price_needed:
					idx = np.where(self.target_symbol_data["Close"] == self.dataclose[0])
					self.config['base_currency_price'] = self.dataclose[0] # TODO CHANGE HERE
				else:
					self.config['base_currency_price'] = self.dataclose[0] # TODO CHANGE HERE

				self.config['price'] = self.dataopen[0]

				# base, target, order, price, base_price, risk, atr, balance
				self.trade_parameters
				# BUY, BUY, BUY!!! (with all possible default parameters)
				self.log('BUY CREATE, %.4f' % self.dataclose[0])

				# Keep track of the created order to avoid a 2nd order
				#self.params['order'] = 'buy'
				self.order = self.buy()

		else:

			if self.dataclose[0] < self.sma[0]:
				# SELL, SELL, SELL!!! (with all possible default parameters)
				self.log('SELL CREATE, %.4f' % self.dataclose[0])

				# Keep track of the created order to avoid a 2nd order
				self.order = self.sell()



